from sugar.activity import activity

import gobject, gtk, pygtk

import sys, os, datetime
sys.path.insert(0,"/home/olpc/Activities/XOtoXO.activity")
import pygame

from time import sleep
from threading import Thread

from toolkit import *
from SugarBar import SugarBar
from HttpManager import HttpManager


BOXES_PAD = 2
gtk.gdk.threads_init()

class XO2XOActivity(activity.Activity):

    def __init__(self, handle):
        print "xo2xo.init"
        activity.Activity.__init__(self, handle)
        toolbox = ActivityToolboxXO2XO(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        # layout the screen
        self._top_canvas_box = View()
        self._top_canvas_box.show()
        box = gtk.HBox(homogeneous=False)
        box.pack_start(self._top_canvas_box)
        box.show_all()
        self.set_canvas(box)

        # to know what id we saw as the last one (will be replaced with new file)
        self.lastQrId = 0
        # the maximum qr-id existing in fing server
        self.maxQrId = 20
        # extension that we know how to treat in act()
        self.imageExtensions = ["png", "jpg", "jpeg", "gif","jpe"]
        self.audioExtensions = ["wav"]

        # http-requests manager
        self.httpManager = HttpManager(self)

        # qr-processor
        self.canLoop = True
        self.exiting = False
        self.sugarbar = SugarBar()
        gobject.timeout_add(20,self.processorLoop)
        
        print "[END]xo2xo.init"

    # implementing write_file
    def can_close(self):
        self.exiting = True
        self.sugarbar.stop()       
        return True

    # looping/looking for qr-codes 
    def processorLoop(self):
        while self.canLoop:
            # process all pending events
            while gtk.events_pending():
                gtk.main_iteration(False)
            # check if we saw some qr-codes
            if not self.exiting:
                self.getQr() 
        print "processorLoop finished"

    # calls SugarBar function that returns an array with decoded qrs
    def getQr(self):
        qrDecodedList = self.sugarbar.getAndAnalize()
        # if it's not an empty array we act
        if(qrDecodedList):
            self.checkForNexoQr(qrDecodedList[0])

    # we check if qr that we saw is nexo-qr (number between 1 and 20)
    def checkForNexoQr(self,qrDecoded):
        try:
            qrDecodedInt = int(qrDecoded)
            if qrDecodedInt in range(1,self.maxQrId+1):
                self.checkForRepeatedQr(qrDecodedInt)
            else:
                self.uknownId()
        except ValueError:
            self.uknownId()

    # we check if it is not the same qr that we saw last time
    # we just act if it if new qr to avoid the situation in which
    # user leave XO in fron of qr
    def checkForRepeatedQr(self,detectedQr):
        if not self.lastQrId == detectedQr:
            self.lastQrId = detectedQr
            toShow = "./pics/detectedQr.png"
            if os.path.isfile(toShow):
                self._top_canvas_box.updateLeft(toShow)
            self.httpManager.getId(detectedQr)
        else:
            print "repeated qr id " + str(detectedQr)

    # play unknown-qr sound
    def uknownId(self):
        self.lastQrId = 0
        toShow = "./pics/unknownQr.png"
        self._top_canvas_box.updateLeft(toShow)
        self._top_canvas_box.updateRight("./pics/test.jpg")
        self.playIt("./sounds/unknown.wav")

    def act(self, filePath):
        ext = filePath.split(".")[-1]
        if ext == "ERROR":
            self.playIt("./sounds/error.wav");
            return
        elif ext == "wav":
            self._top_canvas_box.updateRight("./pics/note.png");
            self.playIt(filePath);
        elif ext in self.imageExtensions:
            self._top_canvas_box.updateRight(filePath);
            self.playIt("./sounds/ready.wav");
        else:
            self._top_canvas_box.updateRight("./pics/file.png");
            self.playIt("./sounds/ready.wav");
        fileName = filePath.split('/')[-1]
        now = datetime.datetime.now()
        nowDateStr = str(now.day) + "/" + str(now.month) + "/" + str(now.year) + "_" + str(now.hour) +":" + str(now.minute) + ":" + str(now.second)
        os.system("copy-to-journal " + filePath + " -t XO2XO_" + nowDateStr + "_" + fileName)

    # to play selected wav file
    def playIt(self, filePath):
        pygame.mixer.init()
        pygame.mixer.music.load(filePath)
        pygame.mixer.music.play()

    def toUploadChosen(self, filePath):
        print "trying to upload" , filePath
        # we saw some qr before?
        if not self.lastQrId == 0:
            # what kind of file is it?
            pathSplit = filePath.split('.')
            splitLen = len(pathSplit)
            extension = pathSplit[splitLen-1]
            if extension in self.imageExtensions:
                self._top_canvas_box.updateRight(filePath)
            elif extension in self.audioExtensions:
                self._top_canvas_box.updateRight("./pics/note.png")
            else:
                self._top_canvas_box.updateRight("./pics/file.png")
            self.httpManager.document_management_service(str(self.lastQrId),filePath)
            self.playIt("./sounds/ready.wav")
        else:
            self.playIt("./sounds/qrMissing.wav")


