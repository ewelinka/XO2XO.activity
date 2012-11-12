#!/usr/bin/python
import pygame
import gtk

class TestGame(object):
    GRAY = 0x888888
    RED  = 0xAA0000
    WHITE = 0xFFFFFF
    BLUE = 0x0000AA
    colorsArray = [0x888888,0xAA0000,0xFFFFFF,0x0000AA]

    picsFolder="pics"
    qrFolder="QRs"

    QRs = {
        "http://www.qrstuff.com/": "leon.jpg",
        "Ver1": "monos.jpg",
        "Version 2": "rana.jpg",
        "Version 3 QR Code": "vaca.jpg",
        "Version 4 QR Code, up to 50 char": "gato.jpg"}
    def __init__(self, screen):  
        # Tamanio de la actividad
        # screen = pygame.display.get_surface()
        self.screenSize = screen.get_size()
        log.debug("TAMANIO: "+str(self.window[0])+", "+str(self.window[1]))

        pygame.init()
        self.screen = screen
        self.screen.fill(self.GREY)
        pygame.display.flip()
        scanFolder(self.qrFolder)
      
    def loadPic(toShow,ventana):
        fileToShow = os.path.join(toShow)
        surface = pygame.image.load(fileToShow)

        #ventana = pygame.display.get_surface()
        ventana.blit(surface, (0,0))

        pygame.display.flip()

    def scanFolder(folderToScan):
        dirList=os.listdir(folderToScan)
        for fname in dirList:
            print fname
            pil = Image.open(folderToScan+"/"+fname).convert('L')
            width, height = pil.size
            raw = pil.tostring()

            # wrap image data
            image = zbar.Image(width, height, 'Y800', raw)

            # scan the image for barcodes
            scanner.scan(image)

            # extract results
            for symbol in image:
                # do something useful with results
                print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

                toReproduce = QRs[symbol.data]
                loadPic(self.picsFolder+"/"+toReproduce, ventana)

            # clean up
            del(image)