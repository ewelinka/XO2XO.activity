import pygtk
import gtk
from sugar.activity import activity
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolbox import Toolbox
from sugar.graphics.objectchooser import ObjectChooser
import sugar.graphics.style as style
import pygame, logging
import gobject


BOXES_PAD = 2

class XO2XOActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        print "***************** estoy en XO2XOActivity! *****************"
        toolbox = ActivityToolboxXO2XO(self)
        self.set_toolbox(toolbox)
        toolbox.show()        # remove any children of the window that Sugar may have added

        #self._top_canvas_box = gtk.HBox(homogeneous=False)
        #

        self._top_canvas_box = View()
        self._top_canvas_box.show()

        # layout the screen
        box = gtk.VBox(homogeneous=False)
        box.pack_start(self._top_canvas_box)
        box.show_all()
        self.set_canvas(box)
        print "----------- estoy en XO2XOActivity! ---------------------"

class ActivityToolbarXO2XO(gtk.Toolbar):
    """The Activity toolbar with the Journal entry title, sharing
       and Stop buttons

    All activities should have this toolbar. It is easiest to add it to your
    Activity by using the ActivityToolbox.
    """
    print "***************** estoy en ActivityToolbarXO2XO! *****************"
    def __init__(self, activity, orientation_left=False):
        gtk.Toolbar.__init__(self)

        self._activity = activity
        #if activity.metadata:
        #    title_button = TitleEntry(activity)
        #    title_button.show()
        #    self.insert(title_button, -1)
        #    self.title = title_button.entry

        if orientation_left == False:
            separator = gtk.SeparatorToolItem()
            separator.props.draw = False
            separator.set_expand(True)
            self.insert(separator, -1)
            separator.show()
        self._object_insert = ToolButton('object-insert')
        self.insert(self._object_insert, -1)
        self._object_insert.show()
        self.stop = StopButton(activity)
        self.insert(self.stop, -1)
        self.stop.show()

        self._object_insert.connect('clicked', self.insertImage, activity)
        print "----------- estoy en ActivityToolbarXO2XO! ---------------------"

    def insertImage(self, widget, activity):
        
        chooser = ObjectChooser('Choose image', self._activity,
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        try:
            result = chooser.run()
            if result == gtk.RESPONSE_ACCEPT:
                logging.debug('ObjectChooser: %r' % chooser.get_selected_object())
                jobject = chooser.get_selected_object()
                if jobject and jobject.file_path:
                    self._activity.game.loadPic(jobject.file_path)
                    #self._activity.screen.loadImage(jobject.file_path)
        finally:
            chooser.destroy()
            del chooser


class ActivityToolboxXO2XO(Toolbox):
    print "***************** estoy en ActivityToolboxXO2XO! *****************"
    def __init__(self, activity):
        Toolbox.__init__(self)

        self._activity_toolbar = ActivityToolbarXO2XO(activity)
        self.add_toolbar('Activity', self._activity_toolbar)
        self._activity_toolbar.show()
        print "----------- estoy en ActivityToolboxXO2XO! ---------------------"
    def get_activity_toolbar(self):
        return self._activity_toolbar


class StopButton(ToolButton):

    def __init__(self, activity, **kwargs):
        ToolButton.__init__(self, 'activity-stop', **kwargs)
        self.props.tooltip = 'Stop'
        self.props.accelerator = '<Ctrl>Q'
        self.connect('clicked', self.__stop_button_clicked_cb, activity)

    def __stop_button_clicked_cb(self, button, activity):
        activity.close()


class View(gtk.EventBox):
    def __init__(self, fill_color=style.COLOR_BUTTON_GREY):
        print "***************** estoy en View! *****************"
        gtk.EventBox.__init__(self)

        self.fill_color = fill_color

        # make an empty box 
        self._leftBox= gtk.HBox()
        self._leftBox.show()

        # make an empty box 
        self._rightBox= gtk.HBox()
        self._rightBox.show()

        # layout the screen
        box = gtk.VBox(homogeneous=False)
        box.pack_start(self._leftBox)
        box.pack_start(self._rightBox, False)
        box.set_border_width(BOXES_PAD)
        self.modify_bg(gtk.STATE_NORMAL, self.fill_color.get_gdk_color())
        self.add(box)
        print "----------- estoy en View! ---------------------"


    def update(self):
        print "***************** estoy en View update! *****************"
        leftPic = gtk.VBox()      
        image = gtk.Image()
        image.set_from_file("test.jpg")
        leftPic.pack_start(image)
        self._leftBox.append(leftPic)
        self._leftBox.pack_start(leftPic, padding=BOXES_PAD)
        leftPic.show()

        rightPic = gtk.VBox()
        image = gtk.Image()
        image.set_from_file("test.jpg")
        leftPic.pack_start(image)
        self._rightBox.append(rightPic)
        self._rightBox.pack_start(rightPic, padding=BOXES_PAD)
        rightPic.show()
        print "----------- estoy en View update! ---------------------"

