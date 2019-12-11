from .base import *
from . import gitlib
import os

def open():

	def choice_not_valid_menu():
		print ("Invalid choice!")

	def add_local_repo_menu():
		folder = input ("Local folder/repo:~>>> ").replace("\"","")

		if not os.path.isdir(folder):
			print ("Invalid folder/repo!")
			return

		if gitlib.init_folder(folder) and DEBUG:
			print ("Init Folder - Success")
		elif DEBUG:
			print ("Init Folder - Failed")





	# Main Menu
	def main_menu():
		print ("######","GitBackup v"+VERSION,"-","Main Menu","######")
		print (" 1)","Add new local repo")

		valid = None

		while valid == None or not valid:
			valid = True
			choice = input(">>> ")
			if choice == "1":
				add_local_repo_menu()
			else:
				valid = False

			if valid == False:
				choice_not_valid_menu()

	main_menu()