#class download
#program : Devildron Secure Download Manager
#Author: C.Velvindron
#Purpose:takes url from main gui and downloads the file

import urllib2 #imports for handling download of file
import threading #handling multple downloads
import os,sys
import time
import logging,ctypes
import requests
import urllib2,hashlib,urllib,re,difflib,string
import urlparse
import os,sys,time,mimetypes,shutil
from decimal import *
from os import path, access, R_OK
import urlgrabber
logger = logging.getLogger(__name__)
temporary_extension = ".temp"
from Tkinter import *
import ttk
import thread
filelog_ext=".log"
path = "C:\sdmdownloads"
status_done = "Completed"
import fileinput

class Downloader(threading.Thread,Tk):
    def __init__(self, path, url, filename,md5url):
        threading.Thread.__init__(self)
        self.max_speed = 0
        #self.link_parser = parser
        #self.status = status #status of file
        self.path = path #local path for saving file current working directory
        self.url = url #download url
        self.filename = filename #filename from gui
        self.flag_stop = False # is download stopped or not 
        self.begin_time = time.time() #time of start of download
        self.ETA = 0 #estimated time remaining for download
        self.total_size = 0
        self.actual_size = 0
        self.speed = 0
        self.tempdlsize = 0 #file size already downloaded
        self.rangeoffile = None
        self.curpath = ""   
        self.block_sz = 512 
        self.time_start= 0
        self.time_end= 0
        self.time_elapsed = 0	
        self.file_md5=""
        self.md5url=md5url
        self.md5found=0	
        self.md5scanned=""		
        #tk.Tk.__init__(self)
        self.tk=Tk()
        self.tk.withdraw()		
        top = Toplevel()
        top.title("Download File Dialog")
   
        msg = Message(top, text=("Downloading file %s" % self.filename))
        msg.pack()
		
        speedlabel=Label(top,text="Speed:",justify="left").pack()		
        self.v = StringVar()        
        Label(top, textvariable=self.v, justify="right").pack()
        
        filemd5label=Label(top,text="File MD5:",justify="left").pack()		
        self.fm = StringVar()        
        Label(top, textvariable=self.fm, justify="right").pack()		
		
        originalmd5label=Label(top,text="MD5 Match:",justify="left").pack()		
        self.orig = StringVar()        
        Label(top, textvariable=self.orig, justify="right").pack()
		
        self.button = Button(top, text="Cancel/Close", command=top.destroy)
        self.button.pack()
        self.button2 = Button(top, text="Calculate MD5/Speed",command=self.callback)
        self.button2.pack()		
        self.progress = ttk.Progressbar(top, orient="horizontal",length=200, mode="determinate")
        self.progress.pack()
        self.progress["maximum"] = 100
        self.progress["value"] = 0		
        		
        
        self.bytes = 0
		
    def callback(self):
        
        self.v.set(self.speed)
        self.fm.set(self.file_md5)
        if self.md5found==1:		
           self.orig.set("positive match: File is authentic")
        else:   
           self.orig.set("no match or no md5 provided...open at your own risks")		    

    
    def checkhttplink(self):
	    
            print "start checkhttplink process"	
            print self.url			
            r = requests.get(self.url,stream=True,allow_redirects=True)
            if r.status_code==200:
                print "link valid"
                print "downloading file"
                pass		
            else:
                print "link invalid"
                print r.status_code
                				

		
    def checkifexists(self):
            print "start checkifexists process"        
            self.curpath = os.path.join(self.path,self.filename)
            curpath=self.curpath #curpath path with filename and extension ,path= folder 
			
            if not os.path.exists(self.path): #if folder does not exist  create path
                os.makedirs(self.path)
                print "download path created"  				
                self.download(curpath)			
            #create download directory1			

            elif os.path.exists(self.curpath):
                print "file already exists and completely downloaded"
                dpath=self.curpath				
                self.filealreadyexists(dpath)				
				
            elif os.path.exists("%s%s" % (self.curpath, temporary_extension)): #file exists with a temp extension
                print "file exists with temp extension"			
                #file already exists			
                tmp_size = os.path.getsize("%s%s" % (self.curpath, temporary_extension))
                self.actual_size = tmp_size				
                thread.start_new_thread(self.download(curpath,True))          
            #sys.exit(0)
			
            else:#folder exists just download
                print "folder only exists"			
                self.download(curpath)

    def filealreadyexists(self,dpath):
        MessageBox = ctypes.windll.user32.MessageBoxA
        MessageBox(None, 'File already exists', 'Download complete!', 0)
        self.progress["value"] = 100		
        md=self.md5_for_file()
        self.file_md5=md	
        self.md5scanned=self.scanreferrerurl()
        #print self.md5scanned			
        self.md5found= self.comparemd5()
   
    def download(self,curpath,Resume=False):
        #take url and download
        #print curpath  		
        os.chdir(self.path)
        #print self.path		
        print "start download process" 		
        if Resume:
		    writemode= "ab"
        else:
            writemode="wb"
        u = urllib2.urlopen(self.url)

        #downloaded file size = file_size_dl
        meta=u.info()
        self.total_size=meta.getheaders("Content-Length")[0]
        print u.info	
        self.total_size = int (self.total_size)		
	
        z=urllib2.Request(self.url)	
        z.add_header("Range","bytes=%s-%s"%(self.actual_size,self.total_size))
        u= urllib2.urlopen(z)
        self.time_start=time.time()		
        f = open("%s%s" % (self.filename,temporary_extension), writemode)        	
        while True:
            buffer = u.read(self.block_sz)
            if not buffer:
                break
            self.actual_size += len(buffer)
            f.write(buffer)
            percentage = (self.actual_size*100)/self.total_size	
            self.progress["value"] =percentage
            			
        f.close()
        self.time_end=time.time()

     		
		#remove .temp extension on file
        print "removing temporary extension"		
        if self.actual_size == self.total_size:
            print "file size check matches"		
            print "calculate time"		
            os.rename("%s%s" % (self.filename, temporary_extension), self.filename)			
            #endtime
            elapsed_time=self.time_end-self.time_start
            self.speed = self.total_size/elapsed_time
            self.speed = self.speed/1000
            print ("Download Speed is %i" % self.speed)
            md=self.md5_for_file()
            self.file_md5=md	
            self.md5scanned=self.scanreferrerurl()
            print self.md5scanned			
            self.md5found= self.comparemd5()
#write completed to log
            s = open("%s\%s%s" % (path,self.filename,filelog_ext)).read()
            #print ("path","%s\%s%s" % (path,self.filename,filelog_ext))					
            s=s.replace('Incomplete','Completed')
            f = open("%s\%s%s" % (path,self.filename,filelog_ext),'w')
            f.write(s)		
            #print ("%s\%s%s" % (path,filename,filelog_ext))		
            f.close()			
            MessageBox = ctypes.windll.user32.MessageBoxA
            MessageBox(None, 'All done', 'Download complete!', 0)               
            
					
        sys.exit(0)	
		
    def md5_for_file(self):
        md5 = hashlib.md5()
        # print x check for file path
        with open(self.curpath,'rb') as f: 
            for chunk in iter(lambda: f.read(128), b''): 
                md5.update(chunk)
        return md5.hexdigest()

    def scanreferrerurl(self):
        print "scanreferrer started"	
        htmlpage=urllib2.urlopen(self.md5url).read()
        results = re.findall(r'(?=(\b[A-Fa-f0-9]{32}\b))',htmlpage)
        return results
		
    def comparemd5(self):
	
        print "***********************"
        print "Performing MD5 Checksum"   
        print "***********************"
        md5found=0
        try:
            self.md5url= self.md5scanned
            print "urlsfound", self.md5url		
            origmd5=[item.lower() for item in self.md5url]
            x=string.join(origmd5)
        #self.file_md5=md5_for_file(file_name)
            print "original md5 is",x
            print "downloader file md5 is",self.file_md5
            print "***********************"
            s = difflib.SequenceMatcher(None, x, self.file_md5)
            print "ratio is:",s.ratio()
            absratio = 0.42 
            if s.ratio > absratio :
                print "--MD5 ratio check--"	
                print "Match found"
                print "--Scanning page for md5--"
                if self.file_md5.lower() in (s.lower() for s in origmd5):
                    print '%s was found on page... MD5 Verification completed successfully' % self.file_md5	
                    md5found = 1					
            else:
                print "Match not found, either file has been corrupt or corresponding page does not contain md5"
                print "you may try to open the file! at your own risk"			
                print "***********************"
                md5found=0
        except:
            print "no md5 found on page"   	
        return md5found