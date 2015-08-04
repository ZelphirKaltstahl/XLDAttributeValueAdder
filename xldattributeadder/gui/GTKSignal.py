__author__ = 'xiaolong'

from enum import Enum

class GTKSignal(Enum):
	CLICKED = "clicked"
	DELETE_EVENT = "delete-event"
	ACTIVATE = "activate"
	DESTROY = "destroy"
	CHANGED = "changed" # for any changes
	TOGGLED = "toggled" # for example checkboxes are toggled between the two states checked and unchecked