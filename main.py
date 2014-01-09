import web
from web import form
web.config.debug = False
import dropbox
import easygui
import time
import webbrowser
from DropboxPython import DropboxPython_Scott

class index:
	
	x = DropboxPython_Scott()

	x.setup()
	x.connect()
	x.download_and_upload_db()
