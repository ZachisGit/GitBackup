from .base import *
import os
import json
import subprocess

class RepoConfig(object):

	initialized = False

	# Initialize if no config file exists yet
	# @param repo_path_url:		local=directory on computer; 
	#							url=remote (github) url for repository;
	# @param repo_name:			repository name and archive folder (ARCHIVE_DIR/repo_name/)
	# @param is_local:			True=local folder based repository;
	#							False=url (github) based repository;
	# [!]
	def __init__(self,repo_path_url,repo_name,is_local,computer_id=None):
		self.repo_path = repo_path_url if is_local else None
		self.repo_url = repo_path_url if not is_local else None
		self.repo_name = repo_name
		self.is_local = is_local
		self.source = "local" if self.is_local else "url"
		self.computer_id = RepoConfig.get_current_computer_id() if computer_id is None else computer_id

		self.initialized = True

	@staticmethod
	def get_current_computer_id():
		# Windows
		if os.name == "nt":
			current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
			return current_machine_id if not current_machine_id is None else "-1"
		return "-1"

	@property
	def archive_path(self):
		return ARCHIVE_DIR+"/"+self.repo_name
	

	@classmethod
	def from_repo_name(cls,repo_name):
		return cls.from_file(ARCHIVE_CONFIG_DIR+"/"+repo_name+".json")


	@classmethod
	def from_file(cls,config_file):
		if not os.path.isfile(config_file):
			return None

		with open(config_file,"r") as file:
			raw = file.read()

		config_json = json.loads(raw)

		# [!]
		rc = cls(repo_path_url="",repo_name="",is_local=False)
		key2param = rc._key2param_table()		
		integrity = rc._json_integrity_check(config_json)

		if not integrity:
			return None

		# Set variables in rc
		for k,v in key2param.items():
			v(rc,config_json[k])

		return rc


	def save(self):
		config_json = {}
		key2param = self._key2param_table()

		for k,v in key2param.items():
			config_json[k] = v(self)

		if not os.path.isdir(ARCHIVE_CONFIG_DIR):
			os.mkdir(ARCHIVE_CONFIG_DIR)

		with open(ARCHIVE_CONFIG_DIR+"/"+self.repo_name+".json","w") as file:
			file.write(json.dumps(config_json))

		return True


	# [!]
	def _key2param_table(self):
		def _local_path(self,v=None):
			if v is None: return self.repo_path
			else: self.repo_path = v
		def _remote_url(self,v=None):
			if v is None: return self.repo_url
			else: self.repo_url = v
		def _repo_name(self,v=None):
			if v is None: return self.repo_name
			else: self.repo_name = v
		def _source(self,v=None):
			if v is None: return self.source
			else: self.source = v
		def _is_local(self,v=None):
			if v is None: return self.is_local
			else: self.is_local = v
		def _computer_id(self,v=None):
			if v is None: return self.computer_id
			else: self.computer_id = v

		table = {
			"local_path": _local_path,
			"remote_url": _remote_url,
			"repo_name": _repo_name,
			"source": _source,
			"is_local": _is_local,
			"computer_id": _computer_id
		}
		return table

	def _json_integrity_check(self,config_json):
		key2param = self._key2param_table()

		for k,v in key2param.items():
			if not k in config_json:
				return False
		return True