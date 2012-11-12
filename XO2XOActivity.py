import pygtk
import gtk
from sugar.activity import activity
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolbox import Toolbox
from sugar.graphics.objectchooser import ObjectChooser
import TestGame
import pygame, logging


class XO2XOActivity(activity.Activity):
    RED  = 0xAA0000

    def __init__(self, handle):
        print "running activity init", handle
        activity.Activity.__init__(self, handle)
        print "activity running"

        toolbox = ActivityToolboxXO2XO(self)
        self.set_toolbox(toolbox)
        toolbox.show()
        
        self.size = (800,600)
        self.screen = pygame.display.set_mode(self.size)
        
        # inicio el juego para que se vea algo
        self.juego = TestGame(self.screen)

        print "AT END OF THE CLASS"

class ActivityToolbarXO2XO(gtk.Toolbar):
    """The Activity toolbar with the Journal entry title, sharing
       and Stop buttons

    All activities should have this toolbar. It is easiest to add it to your
    Activity by using the ActivityToolbox.
    """
    print "***************** estoy aca! *****************"
    def __init__(self, activity, orientation_left=False):
        gtk.Toolbar.__init__(self)

        self._activity = activity
        print "***************** estoy aca! 2 *****************"
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
        print "***************** estoy aca!3 *****************"
        self._object_insert = ToolButton('object-insert')
        self.insert(self._object_insert, -1)
        self._object_insert.show()
        print "***************** estoy aca!4 *****************"
        self.stop = StopButton(activity)
        self.insert(self.stop, -1)
        self.stop.show()

        self._object_insert.connect('clicked', self.insertImage, activity)

    def insertImage(self, widget, activity):
        
        chooser = ObjectChooser('Choose image', self._activity,
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        try:
            result = chooser.run()
            if result == gtk.RESPONSE_ACCEPT:
                logging.debug('ObjectChooser: %r' % chooser.get_selected_object())
                jobject = chooser.get_selected_object()
                if jobject and jobject.file_path:
                    self._activity.area.loadImage(jobject.file_path)
        finally:
            chooser.destroy()
            del chooser

class ActivityToolboxXO2XO(Toolbox):

    def __init__(self, activity):
        Toolbox.__init__(self)

        self._activity_toolbar = ActivityToolbarXO2XO(activity)
        self.add_toolbar('Activity', self._activity_toolbar)
        self._activity_toolbar.show()

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