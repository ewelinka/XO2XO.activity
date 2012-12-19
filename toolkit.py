from sugar.activity import activity
import gtk 
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolbox import Toolbox
from sugar.graphics.objectchooser import ObjectChooser
import sugar.graphics.style as style
BOXES_PAD = 2



class ActivityToolbarXO2XO(gtk.Toolbar):
    def __init__(self, activity, orientation_left=False):
        gtk.Toolbar.__init__(self)

        self._activity = activity
        if orientation_left == False:
            separator = gtk.SeparatorToolItem()
            separator.props.draw = False
            separator.set_expand(True)
            self.insert(separator,-1)
            separator.show()

        self._object_insert = ToolButton('object-insert')
        self.insert(self._object_insert, -1)
        self._object_insert.show()
        self.stop = StopButton(activity)
        self.insert(self.stop, -1)
        self.stop.show()
        self._object_insert.connect('clicked', self.insertImage, activity)

    def insertImage(self, widget, activity):
        self._activity = activity
        chooser = ObjectChooser('Choose image', self._activity,
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        try:
            result = chooser.run()
            if result == gtk.RESPONSE_ACCEPT:
                jobject = chooser.get_selected_object()
                if jobject and jobject.file_path:
                    self._activity.toUploadChosen(jobject.file_path)

        finally:
            chooser.destroy()
            del chooser


class ActivityToolboxXO2XO(Toolbox):
    def __init__(self, activity):
        print "ActivityToolboxXO2XO.init"
        Toolbox.__init__(self)

        self._activity_toolbar = ActivityToolbarXO2XO(activity)
        self.add_toolbar('Activity', self._activity_toolbar)
        self._activity_toolbar.show()
        print "[END]ActivityToolboxXO2XO.init"
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
        print "View.init"
        gtk.EventBox.__init__(self)

        self.fill_color = fill_color

        # make an empty box and everything for the left box
        self._leftBox= gtk.HBox()
        self._leftBox.show()
        self.leftPicBox = gtk.HBox() 
        self.leftPic = gtk.Image()
        fixLeft = gtk.Fixed()  
        fixLeft.put(self.leftPic, 20, 20)
        self.leftPicBox.add(fixLeft)
        #self.leftPicBox.pack_start(self.leftPic)
        self._leftBox.pack_start(self.leftPicBox)
        self.leftPic.show()

        # make an empty box 
        self._rightBox= gtk.HBox()
        self._rightBox.set_size_request(1000, 900)
        self._rightBox.show()
        self.rightPicBox = gtk.HBox() 
        self.rightPic = gtk.Image()
        fixRight= gtk.Fixed()  
        fixRight.put(self.rightPic, 60, 20)
        self.rightPicBox.add(fixRight)
        #self.rightPicBox.pack_start(self.rightPic)
        self._rightBox.pack_start(self.rightPicBox)
        self.rightPic.show()

        # layout the screen
        box = gtk.HBox(homogeneous=False)
        box.pack_start(self._leftBox)
        box.pack_start(self._rightBox, False)
        box.set_border_width(BOXES_PAD)
        self.modify_bg(gtk.STATE_NORMAL, self.fill_color.get_gdk_color())
        self.add(box)
        self.update()
        print "[END]View.init"


    def update(self):
        print "View.update"
        self.leftPic.set_from_file("./pics/unknownQr.png")
        self.rightPic.set_from_file("./pics/test.jpg")
        print "[END]View.update"

    def updateRight(self,file_path):
        print "View.updateRight"
        self.rightPic.set_from_file(file_path)
        print "[END]View.updateRight"

    def updateLeft(self,file_path):
        print "View.updateLeft"
        self.leftPic.set_from_file(file_path)
        print "[END]View.updateLeft"
