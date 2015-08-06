
def go_up(path):
	return path[:path[:path.rfind('/')].rfind('/')] + '/'

def go_in(path, subfolder):
	return path + subfolder + '/'