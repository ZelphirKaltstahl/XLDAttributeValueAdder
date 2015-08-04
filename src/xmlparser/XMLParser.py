import re
from xml.dom import minidom

from lxml import etree

from src.exceptions.XMLParseException import XMLParserException

__author__ = 'xiaolong'


class XMLParser:
	"""
	This class is a XML parser which can validate xml files against a xml schema definition.
	"""
	
	def __init__ (self):
		pass
	
	def validate_file (self, xsd_filename="log_schema.xsd", xml_filename="log.xml"):
		print('validating XML file ...')
		
		# create a schema document by parsing the content of the xsd file
		xml_schema_document = etree.parse(xsd_filename)
		
		# create a schema using the schema document
		xmlschema = etree.XMLSchema(xml_schema_document)
		
		# create a xml document by parsing the content of the xml file
		xml_document = etree.parse(xml_filename)
		
		# try to validate the file
		return xmlschema.validate(xml_document)
	
	
	def validate_tree(self, xsd_filename, xml_tree):
		print('validating xml tree ...')
		# create a schema document by parsing the content of the xsd file
		xml_schema_document = etree.parse(xsd_filename)
		# create a schema using the schema document
		xmlschema = etree.XMLSchema(xml_schema_document)
		
		return xmlschema.validate(xml_tree)
	
	
	def get_xml_element_tree_root (self, xsd_filename="log_schema.xsd", xml_filename="log.xml"):
		print('searching xml root element')
		
		if self.validate_file(xsd_filename=xsd_filename, xml_filename=xml_filename):
			print('vocable file is valid')
			with open(xml_filename, 'r') as f:
				file_content = f.read()
				
				if file_content.startswith("<?"):
					file_content = re.sub("^\<\?.*?\?\>", '', file_content, flags=re.DOTALL)
				
				return etree.XML(file_content)
		else:
			raise XMLParserException("XML file invalid!")
	
	def write_xml_file (self, file, xml_root_element, xml_declaration=False, pretty_print=False, encoding='unicode', indent='\t'):
		rough_string = etree.tostring(xml_root_element, encoding='unicode', xml_declaration=False)
		reparsed = minidom.parseString(rough_string)
		pretty_printed = reparsed.toprettyxml(indent='\t', encoding='utf-8')
		
		file.write(pretty_printed)
		
		#pretty_printed_xml = etree.tostring(xml_root_element, xml_declaration=xml_declaration, pretty_print=pretty_print, encoding=encoding)
		#if pretty_print: pretty_printed_xml = pretty_printed_xml.replace('  ', indent)
		#file.write(pretty_printed_xml)