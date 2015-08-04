from gi.repository import Gtk
from gi.repository import Gio
import sys
from xldattributeadder.gui.GTKSignal import GTKSignal


class XLDAVA_Window(Gtk.ApplicationWindow):
	
	APPLICATION_WINDOW_TITLE = 'XLD Attribute Value Adder'
	
	# noinspection PyMissingConstructor
	def __init__ (self, app):
		Gtk.Window.__init__(self, title=self.APPLICATION_WINDOW_TITLE, application=app)


class XLDAVA_App(Gtk.Application):
	def __init__ (self):
		Gtk.Application.__init__(self)
	
	def do_activate (self):
		win = XLDAVA_Window(self)
		win.show_all()
	
	def initialize (self):
		# start the application
		Gtk.Application.do_startup(self)
		
		# create a menu
		menu = Gio.Menu()
		# append to the menu three options
		menu.append("New", "app.new")
		menu.append("About", "app.about")
		menu.append("Quit", "app.quit")
		# set the menu as menu of the application
		self.set_app_menu(menu)
		
		
		new_action = Gio.SimpleAction.new("new", None)
		new_action.connect(GTKSignal.ACTIVATE.value, self.new_callback)
		self.add_action(new_action)
		
		
		about_action = Gio.SimpleAction.new("about", None)
		about_action.connect(GTKSignal.ACTIVATE.value, self.about_callback)
		self.add_action(about_action)
		
		
		quit_action = Gio.SimpleAction.new("quit", None)
		quit_action.connect(GTKSignal.ACTIVATE.value, self.quit_callback)
		self.add_action(quit_action)
	
	# callback function for "new"
	def new_callback (self, action, parameter):
		print("This does nothing. It is only a demonstration.")
	
	# callback function for "about"
	def about_callback (self, action, parameter):
		print("No AboutDialog for you. This is only a demonstration.")
	
	# callback function for "quit"
	def quit_callback (self, action, parameter):
		print("You have quit.")
		self.quit()


app = XLDAVA_App()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
