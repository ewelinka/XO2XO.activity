import pygtk
import gtk
from sugar.activity import activity
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolbox import Toolbox
from sugar.graphics.objectchooser import ObjectChooser

import logging

class XO2XOActivity(activity.Activity):
	def hello(self, widget, data=None):
		logging.info('Hello World')

	def __init__(self, handle):
		print "running activity init", handle
		activity.Activity.__init__(self, handle)
		print "activity running"

		# Creates the Toolbox. It contains the Activity Toolbar, which is the
		# bar that appears on every Sugar window and contains essential
		# functionalities, such as the 'Collaborate' and 'Close' buttons.
		toolbox = ActivityToolbox(self)
		self.set_toolbox(toolbox)
		toolbox.show()

		# Creates a new button with the label "Hello World".
		self.button = gtk.Button("Hello World")

		# When the button receives the "clicked" signal, it will call the
		# function hello() passing it None as its argument.  The hello()
		# function is defined above.
		self.button.connect("clicked", self.hello, None)

		# Set the button to be our canvas. The canvas is the main section of
		# every Sugar Window. It fills all the area below the toolbox.
		self.set_canvas(self.button)

		# The final step is to display this newly created widget.
		self.button.show()

		print "AT END OF THE CLASS"

class ActivityToolbar(gtk.Toolbar):
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
        #if activity.metadata:
        #    description_item = DescriptionItem(activity)
        #    description_item.show()
        #    self.insert(description_item, -1)

        #self.share = ShareButton(activity)
        #self.share.show()
        #self.insert(self.share, -1)

        # DEPRECATED
        #self.keep = KeepButton(activity)
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

class ActivityToolbox(Toolbox):
    """Creates the Toolbox for the Activity

    By default, the toolbox contains only the ActivityToolbar. After creating
    the toolbox, you can add your activity specific toolbars, for example the
    EditToolbar.

    To add the ActivityToolbox to your Activity in MyActivity.__init__() do:

        # Create the Toolbar with the ActivityToolbar:
        toolbox = activity.ActivityToolbox(self)
        ... your code, inserting all other toolbars you need, like EditToolbar

        # Add the toolbox to the activity frame:
        self.set_toolbar_box(toolbox)
        # And make it visible:
        toolbox.show()
    """

    def __init__(self, activity):
        Toolbox.__init__(self)

        self._activity_toolbar = ActivityToolbar(activity)
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