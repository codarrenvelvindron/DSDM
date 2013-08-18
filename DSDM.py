#class App
#program : Devildron Secure Download Manager
#Author: C.Velvindron
#Purpose:whole gui for the application

from Tkinter import *
import Pmw
import Tkinter
from download1110 import Downloader
import os
import urlparse
import thread
import subprocess
from multilistbox import *
import glob
hyperlink= "http://"
default_storage_path= "C:\sdmdownloads"
filelog_ext=".log"

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()
        #self.btndownload = Button(frame, text="Download", command=self.dl_dialog)
        #self.btndownload.pack(side=LEFT)

        self.btndlfolder = Button(frame, text="Download folder", command=self.dl_folder)
        self.btndlfolder.pack(side=LEFT)

        self.add_dl = Button(frame, text="Add download",fg="white",bg="black", command=self.add_download)
        self.add_dl.pack(side=LEFT)			

        
        self.curtest = Button(frame, text="Start download",bg="green", command=self.startdl)
        self.curtest.pack(side=LEFT)
        #self.displaybox() #show download displaybox
        
        self.resume = Button(frame, text="Resume download",bg="orange", command=self.startdl)
        self.resume.pack(side=LEFT)
		
        self.delete = Button(frame, text="Delete download",bg="red", command=self.deletedl)
        self.delete.pack(side=LEFT)
		

		
        self.quit = Button(frame, text="QUIT",bg="black", fg="red", command=frame.quit)
        self.quit.pack(side=RIGHT)
		
        self.path= default_storage_path
        self.url= ""
        self.md5url= ""	
        self.filename= ""
        self.validate=""
        self.status="Incomplete"		
        self.mlb = MultiListbox (root,(('filename', 100),('URL', 400),('PATH', 100),('MD5url',10),('Status',10)),height=20,bg='white')
        self.populatequeue()
        self.mlb.pack (expand=YES,fill=BOTH)
              		

	
    def deletedl(self):
        x= self.mlb.curselection()
        y= self.mlb.get(x)
        for items in y:
            filename=y[0]
            path=y[2]
	
        filename=filename.rstrip('\n')
        filename=filename.strip()		

        path=path.rstrip('\n')
        path=path.strip()		
        
        if os.path.exists("%s\%s" % (path,filename)):
            os.remove("%s\%s" % (path,filename))
            os.remove("%s\%s%s" % (path,filename,filelog_ext))		
            self.mlb.delete(x)
        elif os.path.exists("%s\%s%s" % (path,filename,filelog_ext)):			
            os.remove("%s\%s%s" % (path,filename,filelog_ext))		
            self.mlb.delete(x)
        else:
            self.mlb.delete(x)		
		
		
    def startdl(self):	
        
        x= self.mlb.curselection()
        y= self.mlb.get(x)
        for items in y:
            filename=y[0]
            url=y[1]
            path=y[2]
            md5url=y[3]	 	
        filename=filename.rstrip('\n')
        filename=filename.strip()		
        print filename		
        url=url.rstrip('\n')
        url=url.strip()		
        print url		
        path=path.rstrip('\n')
        path=path.strip()		
        print path
        md5url=md5url.rstrip('\n')
        md5url=md5url.strip()		
        print md5url		

        d=Downloader(path,url,filename,md5url)
        thread.start_new_thread(d.checkhttplink, ())
        thread.start_new_thread(d.checkifexists, ())
		
		
    def add_download(self):
        self.dialog = Toplevel(root)
        self.dialog.title("Download Dialog")	
        self.url = Pmw.EntryField(self.dialog,
                labelpos = 'w',
                label_text = 'URL:',
                validate = self.custom_validate,
                value = 'ABC')
        #self.dialog.withdraw()
        self.url.pack()
		
        self.path = Pmw.EntryField(self.dialog,
                labelpos = 'w',
                label_text = 'Path:',
                validate = None,
                value = 'C:\sdmdownloads')
        #self.dialog.withdraw()
        self.path.pack()
		
      
		
        self.md5url = Pmw.EntryField(self.dialog,
                labelpos = 'w',
                label_text = 'MD5 URL:',
                validate = self.custom_validate,
                value = 'http://www.md5.com')
        #self.dialog.withdraw()
        self.md5url.pack()
		
        self.x=Button(self.dialog, text="Download",state=DISABLED,command=self.addqueue)
        self.x.pack(side=LEFT)	
        #print x
        self.y=Button(self.dialog, text="Check URL",state=NORMAL,command=self.callback).pack(side=RIGHT)	
        
        self.mcheck = IntVar()
        c = Checkbutton(self.dialog,state=ACTIVE, text="Disable md5",variable=self.mcheck,command=self.md5disable)
        c.pack()  	
		
    def filename_parse(self,url): #function to extract filename from url
        return os.path.basename(urlparse.urlsplit(url)[2])
	
    #download folder create if does not exist
    def dl_folder(self):
        	
        if not os.path.exists(default_storage_path):
             os.makedirs(default_storage_path)
        subprocess.Popen(r'explorer /select,"C:\sdmdownloads\"')
		
 # Create the dialog.
 		


    def callback(self):	
        if 	"yes" in self.validate:	
            self.x['state'] = 'active'
       	else:    
            self.x['state'] = 'disabled'			
     	 
    def md5disable(self):
        x=self.mcheck.get()		
        print self.mcheck.get()
        if x == 1:
            		    
            self.md5url.pack_forget()
		
        else:
            self.md5url.pack()		

    def custom_validate(self, text):
        print 'text:', text
        if hyperlink in text:
            print "http suceed"
            self.validate=self.validate+"yes"			
            return 1
          
        else:
            		
            print "http fail"		
            return -1

    def populatequeue(self):
        path="C:\sdmdownloads"
        os.chdir(path)
        for files in os.listdir("."):
            if files.endswith(".log"):
        #print files
                filearray=[]
                filearray.append(files)
                #print filearray[0]
        #print filearray[2]		
                for files in filearray:
                    #print file		    
                    f = open("%s\%s" % (path,files),"r")	
                    print ("%s\%s" % (path,files) )			
                    array = []
                    for line in f:
                        array.append( line )
                    f.close()
                    self.mlb.insert (END, ('%s' % (array[0]),'%s' % (array[1]),'%s' % (array[2]),'%s' % (array[3]),'%s' % (array[4])))
                    self.mlb.pack (expand=YES,fill=BOTH)
			


        #current=self.mlb.curselection()
        #print current	
    def addqueue(self):
        		
        #listbox
        #mlb = MultiListbox (root,(('filename', 30),('URL', 400),('PATH', 100),('MD5url',10)),height=20,bg='white')
        #print type(z)
        #self.dialog.destroy()		
        url = self.url.get()	
        path=self.path.get()
        md5url=self.md5url.get()
        print "md5url contents:" + "/" +md5url +"/"		
        filename=self.filename_parse(url)
	
        #write download log		
        f = open("%s\%s%s" % (path,filename,filelog_ext),"w")
        data=("%s \n" % filename,"%s \n" % url,"%s \n" % path,"%s" % md5url,"\n%s" % self.status)		
        f.writelines(data)
        #print ("%s\%s%s" % (path,filename,filelog_ext))		
        f.close()
		
        #f = open("%s%s" % (filename,filelog_ext),"r")
   		
        #read download log
        f = open("%s\%s%s" % (path,filename,filelog_ext),"r")		
        array = []
        for line in f:
            array.append( line )
        f.close()
        self.mlb.insert (END, ('%s' % (array[0]),'%s' % (array[1]),'%s' % (array[2]),'%s' % (array[3]),'%s' % (self.status)))
        self.mlb.pack (expand=YES,fill=BOTH)
        #current=self.mlb.curselection()
        #print current
        self.dialog.destroy()
    

root = Tk()

root.title("Devildron's Secure Download Manager 1.20")
Pmw.initialise(root)
app = App(root)
root.geometry('600x600+500+300')
root.mainloop()