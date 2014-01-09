import web
from web import form
web.config.debug = False
import dropbox
import easygui
import time
import webbrowser

urls = (
	"/", "index"
)

render = web.template.render('templates/')
app = web.application(urls, globals())

class index:

	def GET(self):
		global session, client, request_token, url
		app_key = 'kdn7k7jndg4l9hf'
		app_secret = '8rcriv7n18ss2zu'

		session = dropbox.session.DropboxSession(app_key, app_secret, "dropbox")
		client = dropbox.client.DropboxClient(session)
		request_token = session.obtain_request_token()
		url = session.build_authorize_url(request_token)
		msg = "Opening %s. Please make sure this application is allowed before continuing."
		print msg % url

		return render.doDropbox("")

	def POST(self):
		global session, client, request_token, url
		allFormInputs = web.input()
		print allFormInputs

		buttonDropbox = allFormInputs.buttonDropbox

		if buttonDropbox == "Connect to Dropbox":
			webbrowser.open(url)
			#time.sleep(5)		
			#easygui.msgbox("Close this window to continue", title="Confirmation box")
			return render.doDropbox(buttonDropbox)
			raw_input("Press enter to continue")	
			access_token = session.obtain_access_token(request_token)
	
		# Downloading file
		# minorly changing the file's contents locally	
		elif buttonDropbox == "Download CSV from Dropbox":
			f, metadata = client.get_file_and_metadata('/working-draft.txt')
			out = open('working-draft.txt', "w")
			out.write(f.read() + " scott")
			out.close()
			print "metadata: %s" % metadata

		# Uploading file	
		elif buttonUpload == "Upload amended CSV to Dropbox":
			f = open('working-draft.txt')
			response = client.put_file('/working-draft.txt', f)
			print "uploaded: %s" % response
		
		else:
			a = 5

		#----------
		#flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
		#authorize_url = flow.start()
		#print '1. Go to: ' + authorize_url
		#print '2. Click "Allow" (you might have to log in first)'
		#print '3. Copy the authorization code.'
		#code = raw_input("Enter the authorization code here: ").strip()
		#access_token, user_id = flow.finish(code)
		#client = dropbox.client.DropboxClient(access_token)
		#print 'linked account: ', client.account_info()


app = app.run()
