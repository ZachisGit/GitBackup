import os

VERSION = "1.1912.10.1"
GIT_EXEC = "git"
ARCHIVE_DIR = os.path.abspath("archive/")
ARCHIVE_CONFIG_DIR = os.path.abspath("archive_config/")
DEBUG = True
GIT_CRED_PROGRAM_WIN = "!echo $'host=github.com\\nprotocol=https\\nusername=[GIT_USER]\\npassword=[GIT_PASSWORD]\\n'"
GIT_CRED_PROGRAM = GIT_CRED_PROGRAM_WIN