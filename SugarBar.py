# -*- coding: utf-8 -*-
from ctypes import *
cdll.LoadLibrary("./libzbar.so.0.2.0")
import zbar

import sys
sys.path.insert(0,"/home/olpc/Activities/XOtoXO.activity")
import pygame.camera
from pygame.locals import *


pygame.init()
pygame.camera.init()

class SugarBar:
    SIZE = (320,240)
    def __init__(self):
        print "SugarBar.init"
        self.zImg=[]
        self.cam = pygame.camera.Camera("/dev/video0",self.SIZE, "YUV")
        self.cam.start()

        self.scanner = zbar.ImageScanner()
        self.scanner.parse_config('disable')
        self.scanner.parse_config('qrcode.enable')
        self.scanner.enable_cache(True)

        self.grayImg = pygame.Surface(self.SIZE, depth=8)
        self.grayImg.set_palette([(x, x, x) for x in xrange(255)])
        self.stoppingCam = False
        print "[END]SugarBar.init"

    def stop(self):
        print "Stop that cam!"
        if not self.stoppingCam:
            print "stop it now!"
            self.stoppingCam = True
            self.cam.stop()

    def getAndAnalize(self):
        if self.cam.query_image():
            self.nueva = True
            image = self.cam.get_image()
            arr3d = pygame.surfarray.pixels3d(image)
            lumi = arr3d[0:self.SIZE[0], 0:self.SIZE[1], 0]
            pygame.surfarray.blit_array(self.grayImg, lumi)

            imgString = pygame.image.tostring(self.grayImg, "P")

            self.zImg = zbar.Image(self.SIZE[0], self.SIZE[1], "Y800", imgString)
            self.scanner.scan(self.zImg)           
            
            decoded = []
            for symbol in self.zImg:
                decoded.append(symbol.data)
                print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
                
            return decoded

"""    def main(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False

            self.getAndAnalize()
"""
