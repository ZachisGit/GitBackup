from .base import *
from . import gitlib
import os
from glob import glob
from .repo_config import RepoConfig

def open(auto_update=False):

	def choice_not_valid_menu():
		print ("Invalid choice!")

	def add_local_repo_menu():
		folder = input ("Local folder/repo:~>>> ").replace("\"","")

		if not os.path.isdir(folder):
			print ("Invalid folder/repo!")
			return

		gitlib._clear_empty_repos()
		if gitlib.init_folder(folder) and DEBUG:
			print ("Init Folder - Success")
		elif DEBUG:
			print ("Init Folder - Failed")


	def add_remote_repo_menu():
		url = input ("Remote repository (github):~>>> ").replace("\"","")

		gitlib._clear_empty_repos()	
		if gitlib.init_url(url) and DEBUG:
			print ("Init Url - Success")
		elif DEBUG:
			print ("Init Url - Failed")



	def update_repos_menu():
		print ("Updating local repositories...")
		print ("")

		# Load repo configs
		config_files = glob(ARCHIVE_CONFIG_DIR+"/*.json")

		local_repos = []
		remote_repos = []
		failed_rcs = []
		for i in range(len(config_files)):
			_rc = RepoConfig.from_file(config_files[i])
			if _rc is None or _rc.initialized == False:
				failed_rcs.append(config_files[i])
			else:
				# local and native to same pc
				if _rc.is_local and RepoConfig.get_current_computer_id() == _rc.computer_id:
					# check that repo still exists else place it in failed_rcs
					if not os.path.isdir(_rc.repo_path):
						failed_rcs.append(config_files[i])
						continue
					local_repos.append(_rc)
				else:
					remote_repos.append(_rc)

		print ("[..] loaded repositories:")
		if len(local_repos) > 0: print ("    +" + "\n    +".join([_rc.repo_name + " - local" for _rc in local_repos]))
		if len(remote_repos) > 0: print ("    +" + "\n    +".join([_rc.repo_name + " - remote" for _rc in remote_repos]))
		print ("")
		if len(failed_rcs) > 0:
			print ("[!] failed to load the following repository configs:")
			print ("    -" +"\n    -".join([_rc for _rc in failed_rcs]))
			print ("")

		# UPDATING REPOSITORIES
		# Local
		for i in range(len(local_repos)):
			print ("")
			print ("[..] updating local \""+local_repos[i].repo_name+"\"...")

			if gitlib.update_folder(local_repos[i]) and DEBUG:
				print ("Update local - Success")
			elif DEBUG:
				print ("Update local - Failed")

		# Remote
		for i in range(len(remote_repos)):
			print ("")
			print ("[..] updating remote \""+remote_repos[i].repo_name+"\"...")

			if gitlib.update_url(remote_repos[i]) and DEBUG:
				print ("Update remote - Success")
			elif DEBUG:
				print ("Update remote - Failed")

		print ("[!] Update successfull")



	# Main Menu
	def main_menu():
		print ("######","GitBackup v"+VERSION,"-","Main Menu","######")
		print (" 1)","Add new local repo")
		print (" 2)","Add new remote repo")
		print (" 3)","Update repos")

		valid = None

		while valid == None or not valid:
			valid = True
			choice = input(">>> ")
			if choice == "1":
				add_local_repo_menu()
			elif choice == "2":
				add_remote_repo_menu()
			elif choice == "3":
				update_repos_menu()
			else:
				valid = False

			if valid == False:
				choice_not_valid_menu()

	if not auto_update:
		main_menu()
	else:
		update_repos_menu()
		input ("press any key...")