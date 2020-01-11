from .base import *
from .repo_config import RepoConfig
import os
import subprocess
import shlex
from datetime import datetime

_git_user = ""
_git_password = ""

def _set_creds(u,p):
	global _git_password, _git_user
	_git_user = u
	_git_password = p


def _available_dir_name(base_name):
	# No / or \ on the end of the path
	dir_name = os.path.abspath(base_name)

	idx = None
	while os.path.isdir(dir_name+("_"+str(idx) if not idx is None else "")):
		if idx is None:
			idx = 1
		else:
			idx += 1
	return dir_name+("_"+str(idx) if not idx is None else "")

def _clear_empty_repos():
	if not os.path.isdir(ARCHIVE_DIR):
		return

	list_dir = os.listdir(ARCHIVE_DIR)
	for i in range(len(list_dir)):
		if os.path.isdir(ARCHIVE_DIR+"/"+list_dir[i]) and len(os.listdir(ARCHIVE_DIR+"/"+list_dir[i])) == 0:

			print ("_",ARCHIVE_DIR+"/"+list_dir[i])
			os.rmdir(ARCHIVE_DIR+"/"+list_dir[i])

def _git_folder(folder):
	folder = folder.replace("\\","/")
	if folder[1] == ":":
		return "/"+folder[0]+folder[2:]
	return folder

def _run_command(command,cred_prefix=False):
	if DEBUG:
		print (" ".join([GIT_EXEC]+command))

	subprocess.call([GIT_EXEC]+(_bc_cred_prefix() if cred_prefix else [])+command)

def _bc_clone(source,dest_dir):
	#source = _git_folder(source)
	#dest_dir = _git_folder(dest_dir)
	return ["clone",source,dest_dir]

def _bc_init(dest_dir):
	#dest_dir = _git_folder(dest_dir)
	return ["init",dest_dir]

def _bc_add(repo,file="."):
	#repo = _git_folder(repo)
	return ["-C",repo,"add",file]

def _bc_commit(repo,msg):
	#repo = _git_folder(repo)
	return ["-C",repo,"commit","-m",msg]

def _bc_push(repo):
	#repo = _git_folder(repo)
	return ["-C",repo,"push"]

def _bc_pull(repo):
	#repo = _git_folder(repo)
	return ["-C",repo,"pull"]

def _bc_cred_prefix():
	global _git_user,_git_password
	return shlex.split("-c credential.helper=\""+GIT_CRED_PROGRAM.replace("[GIT_USER]",_git_user).replace("[GIT_PASSWORD]",_git_password)+"\"")

### INITIALIZE REPOSITORIES ###
def init_folder(folder):

	folder = os.path.abspath(folder)

	# Is Git Repository
	is_git_repo = os.path.isdir(folder+"/.git")

	# NOT A GIT REPOSITORY
	if not is_git_repo:
		# git init
		# git add .
		# git commit -m "Repository created by GithubBackup"
		_run_command(_bc_init(folder))
		_run_command(_bc_add(folder))
		_run_command(_bc_commit(folder,"Repository created by GithubBackup"))

	# Clone Repo to local Archive
	archive_name = folder.split("/")[-1].split("\\")[-1]		# Repo name before availability check
	archive_path = _available_dir_name(ARCHIVE_DIR+"/"+archive_name)
	repo_name = archive_path.split("/")[-1].split("\\")[-1]		# Repo name after availability check


	if DEBUG:
		print ("Archive-Path:",archive_path)
		print ("Repo-Name:",repo_name)

	if not os.path.isdir(ARCHIVE_DIR):
		os.mkdir(ARCHIVE_DIR)

	# git clone folder archive/
	_run_command(_bc_clone(folder,archive_path))

	# ADD TO CONFIG
	rc = RepoConfig(repo_path_url=folder,repo_name=repo_name,is_local=True)

	if rc is None:
		return False

	# Check if cloning worked
	if not os.path.isdir(rc.archive_path) or len(os.listdir(rc.archive_path)) == 0:
		return False

	rc.save()

	return True

def init_url(url):

	# Archive name from git link https://github.com/ZachisGit/[BlaBla].git
	archive_name = url.split("/")[-1]
	if archive_name.lower().endswith(".git"):
		archive_name = archive_name[:-4]

	if archive_name == "":
		return False


	# Clone Repo to local Archive
	archive_path = _available_dir_name(ARCHIVE_DIR+"/"+archive_name)
	repo_name = archive_path.split("/")[-1].split("\\")[-1]		# Repo name after availability check


	if DEBUG:
		print ("Archive-Path:",archive_path)
		print ("Repo-Name:",repo_name)

	if not os.path.isdir(ARCHIVE_DIR):
		os.mkdir(ARCHIVE_DIR)

	# git clone folder archive/
	_run_command(_bc_clone(url,archive_path),cred_prefix=True)

	# ADD TO CONFIG
	rc = RepoConfig(repo_path_url=url,repo_name=repo_name,is_local=False)

	if rc is None:
		return False

	# Check if cloning worked
	if not os.path.isdir(rc.archive_path) or len(os.listdir(rc.archive_path)) == 0:
		return False

	rc.save()

	return True



### UPDATE REPOSITORIES ###
def update_folder(rc):

	if rc is None or rc.initialized == False:
		return False

	# git -C LOCAL_FOLDER add .
	# git -C LOCAL_FOLDER commit -m "Local backup yyyy:mm:dd hh:mm:ss"
	# git -C ARCHIVE pull
	_run_command(_bc_add(rc.repo_path))
	_run_command(_bc_commit(rc.repo_path,"Local backup "+ datetime.now().strftime("%Y_%m_%d %H:%M:%S")))
	_run_command(_bc_pull(rc.archive_path))

	return True

def update_url(rc):

	if rc is None or rc.initialized == False:
		return False

	# git -C ARCHIVE pull
	_run_command(_bc_pull(rc.archive_path),cred_prefix=True)

	return True