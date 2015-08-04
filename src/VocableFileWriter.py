from lxml import etree
from src import XMLInvalidException, XMLParser

__author__ = 'xiaolong'

class VocableFileWriter():
	
	def __init__(self):
		pass
	
	@staticmethod
	def write(self, xsd_file_path, vocable_file_path, xml_root):
		#print('writing xml to vocable file ...')
		xml_parser = XMLParser()
		if xml_parser.validate_tree(xsd_file_path, xml_root):
			try:
				with open(vocable_file_path, 'w') as file:
					file.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n\n")
					file.write(etree.tostring(xml_root, xml_declaration=False, pretty_print=True, encoding="unicode"))
			except IOError:
				print("Error while writing in log file!")			
		else:
			print("Tree is invalid.")
			raise XMLInvalidException('Invalid XML!')