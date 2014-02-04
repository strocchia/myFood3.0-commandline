#import web
#from web import form
#web.config.debug = False
#import easygui
import dropbox
import time
import webbrowser
from DropboxPython import DropboxPython_Scott

class index:
	
	x = DropboxPython_Scott()

#five five five

	x.setup()
	x.connect()
	x.download_and_upload_db()
