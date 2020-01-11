import sys
import os
from code.base import *
from code.repo_config import RepoConfig
from code import gitlib

os.environ["PATH"] += ";"+os.path.abspath("win\\PortableGit-2.24.0.2-32-bit.7z\\bin\\")

GIT_EXEC = "git.exe"
GIT_CRED_PROGRAM = GIT_CRED_PROGRAM_WIN

from code import menu

menu.open(ask_creds=True)

""" RepoConfig tests
#rc = RepoConfig(repo_path_url="path_url",repo_name="repo_name",is_local=True)
rc = RepoConfig.from_repo_name("local_repo")
if rc is None:
	print ("RepoConfig failed integrity check!")
else:
	print (rc.repo_path)
	print (rc.repo_url)
	print (rc.repo_name)
	print (rc.archive_path)
	print (rc.is_local)
	print (rc.source)
	print (rc.computer_id)
	print ("")
	#print (rc.save())
#"""


""" Git run command tests
import subprocess


print ("!!IMPORTANT!!:","Choose \"wincred\" and select Allways choose...")
subprocess.call(["git.exe","clone","https://github.com/ZachisGit/WikiToolBoxHosting.git"])

subprocess.call(["git.exe","clone","https://github.com/ZachisGit/Wahl-Tag-Date.git"])
#"""