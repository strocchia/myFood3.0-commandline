#import web
#from web importori#m
#import easygui
#web.config.debug = False
#import easygui
import csv
import dropbox
import time
import webbrowser

#urls = (
#	"/", "index"
#)

#render = web.template.render('templates/')
#app = web.application(urls, globals())

class DropboxPython_Scott:

	def __init__(self):
		self.last_date = ""
		self.last_lunch = 0.0
		self.last_dinner = 0.0
		self.last_misc = 0.0
		self.writeArray = ["", "", "", ""]

	def setup(self):
		print "If this is the first time you are opening this console-based application, please download this file and place it into a /foodtracking directory of your Dropbox folder: http://depositfiles.com/files/tcvx2y5yt."

		self.app_key = 'kdn7k7jndg4l9hf'
		self.app_secret = '8rcriv7n18ss2zu'

		self.session = dropbox.session.DropboxSession(self.app_key, self.app_secret, "dropbox")
		self.client = dropbox.client.DropboxClient(self.session)
		self.request_token = self.session.obtain_request_token()
		self.url = self.session.build_authorize_url(self.request_token)
		self.msg = "Opening %s. Please make sure this application is allowed before continuing."
		print self.msg % self.url

	def connect(self):
		webbrowser.open(self.url)
		#time.sleep(3)
		#easygui.msgbox("Close this window, and return to your Terminal window to continue", title="Confirmation box")
		print ""
		raw_input("Press Enter key to continue forward")
		print ""
		self.access_token = self.session.obtain_access_token(self.request_token)
	
	# Downloading file
	def downloaddb(self, filenameToDownload):
		f, metadata = self.client.get_file_and_metadata('/foodtracking/' + filenameToDownload)
		out = open(filenameToDownload, "wb")
		out.write(f.read())
		out.close()
		# just debugging
		#print "metadata: %s" % metadata

	# Uploading file
	def uploaddb(self, filenameToUpload):
		f = open(filenameToUpload)
		response = self.client.put_file('/foodtracking/' + filenameToUpload, f, overwrite = True)
		# just debugging, again
		#print "uploaded: %s" % response
	
	# Downloading, amending, uploading file
	def download_and_upload_db(self):
		self.downloaddb('newcsv.csv')
		
		date = raw_input("1. Enter date on which meal was consumed (mm/dd/yyyy): ")
		mealtype = raw_input("2. Enter meal data in order, according to the following hierarchy (L = Lunch / D = Dinner / M = Miscellaneous): ")
		if mealtype == "L" or mealtype == "l":
			lunch = raw_input("3. Enter amount spent on lunch: $")
		elif mealtype == "D" or mealtype == "d":
			dinner = raw_input("3. Enter amount spent on dinner: $")
		elif mealtype == "M" or mealtype == "m":
			misc = raw_input("3. Enter miscellaneous spending amount: $")
		else:
			print "invalid input. Try running the program again."
		print ""		

        	with open('newcsv.csv', 'r') as fp1:
                	firstlinebegin = fp1.readline()
                	lineresponsebegin = fp1.readlines()
        	fp1.close()
           
		lineresponsebegin = [x.strip() for x in lineresponsebegin]

		readarray = []
		for x in lineresponsebegin:
			readarray.append(x.split(','))
 
		datelist = []
		lunchlist = []
		dinnerlist = []
		misclist = []

        	for i in readarray:
        		# for debugging purposes ONLY
			#print "i (of readarray): %s" % i

            		# populate lists with data that already exists in the CSV file
            		datelist.append(i[0])
            		if i[1] != '':
                		lunchlist.append(i[1])
            		if i[2] != '':
                		dinnerlist.append(i[2])
           		if i[3] != '':
                		misclist.append(i[3])
                
		if not date in datelist:
			datelist.append(date)
		if mealtype == "L" or mealtype == "l":
			lunchlist.append(lunch)
		elif mealtype == "D" or mealtype == "d":
			dinnerlist.append(dinner)
		elif mealtype == "M" or mealtype == "m":
			misclist.append(misc)
        	else:
            		print "wrong input, re-run command-line program"

        	CSVrows = map(None, datelist, lunchlist, dinnerlist, misclist)
            
		with open('newcsv.csv', 'wb') as fp2:
        		writer = csv.writer(fp2)
            		writer.writerow(['Date', 'Lunch', 'Dinner', 'Miscellaneous'])
            		for j in CSVrows:
                		writer.writerow(j)
		fp2.close()			

		self.uploaddb('newcsv.csv')
