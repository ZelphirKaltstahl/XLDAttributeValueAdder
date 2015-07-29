"""__author__ = 'xiaolong'

from gi.repository import Gtk

class XLDAttributeAdderWindow():
	
	def __init__(self):
		Gtk.Window.__init__(self, title="Livestreamer GTK+ 3 GUI")
		win = Gtk.Window()
		win.connect("delete-event", Gtk.main_quit)
		win.show_all()
		Gtk.main()
	
	
	def abc(self):
		Gtk."""
	