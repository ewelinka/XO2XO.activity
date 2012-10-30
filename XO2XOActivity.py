import pygtk
import gtk
from sugar.activity import activity

class XO2XOActivity(activity.Activity):
	def __init__(self, handle):
		"The entry point to the Activity"
		activity.Activity.__init__(self, handle)
		toolbox = activity.ActivityToolbox(self)
        activity_toolbar = toolbox.get_activity_toolbar()
        activity_toolbar.keep.props.visible = False
        activity_toolbar.share.props.visible = False
        self.set_toolbox(toolbox)

        toolbox.show()