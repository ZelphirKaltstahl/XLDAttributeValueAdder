__author__ = 'xiaolong'

from gi.repository import Gtk
class XLDAttributeValueAdderWindow(Gtk.Window):
	
	def __init__(self):
		Gtk.Window.__init__(self, title="XLD Attribute Value Adder")
		self.initialize()
	
	
	def initialize (self):
		win = Gtk.Window()
		win.connect("delete-event", Gtk.main_quit)
		win.show_all()
		Gtk.main()

