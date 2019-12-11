from .base import *
from .repo_config import RepoConfig
import os
import subprocess

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



def _run_command(command):
	if DEBUG:
		print (" ".join([GIT_EXEC]+command))

	subprocess.call([GIT_EXEC]+command)

def _bc_clone(source,dest_dir):
	return ["clone",source,dest_dir]

def _bc_init(dest_dir):
	return ["init",dest_dir]

def _bc_add(repo,file="."):
	return ["-C",repo,"add",file]

def _bc_commit(repo,msg):
	return ["-C",repo,"commit","-m",msg]

def _bc_push(repo):
	return ["-C",repo,"push"]

def _bc_pull(repo):
	return ["-C",repo,"pull"]



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

	rc.save()

	return True

