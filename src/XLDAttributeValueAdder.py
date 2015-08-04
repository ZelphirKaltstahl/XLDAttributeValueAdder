import re

from lxml import etree
from src.WordListHelper import WordListHelper
from src.WordListReader import WordListReader
from src.exceptions.XMLInvalidException import XMLInvalidException

from src.exceptions.XMLParseException import XMLParserException
from src.xmlparser import XMLParser

__author__ = 'xiaolong'


class XLDAttributeAdder():
	
	# initialize with default value
	vocable_file_path = 'vocables.xml'
	xsd_file_path = 'xld-vocables-schema.xsd'
	word_list_file_path = 'words'
	
	ATTRIBUTE_SEPARATOR = '/'
	VOCABLE_ATTRIBUTE_VALUE_PLACEHOLDER = '---'
	
	xml_parser = None
	
	xml_root = None
	
	
	def __init__(self, vocable_file_path, xsd_file_path, word_list_file_path):
		self.vocable_file_path = vocable_file_path
		self.xsd_file_path = xsd_file_path
		self.word_list_file_path = word_list_file_path

	
	def add_values_to_attribute_of_vocables (self, attribute_name, attribute_value, words_attribute_name):
		print('trying to add value to attribute of the vocables ...')
		list_of_words = WordListReader.read(WordListReader, self.word_list_file_path)
		
		# create a dict to be able to tell which vocables haven't been found and subsequently didn't get any new attribute value
		words_added = {}
		for word in list_of_words:
			words_added[word] = False
		
		add_counter = 0
		
		print('list of words')
		for word in list_of_words:
			print(word, ',', sep='', end='\n')
		
		print('creating XMLParser instance')
		self.xml_parser = XMLParser()
		
		try:
			self.xml_root = self.xml_parser.get_xml_element_tree_root(self.xsd_file_path, self.vocable_file_path)
			
			for vocable in self.xml_root:
				# if this is one of the vocables, which need to be changed
				#if vocable.find(words_attribute_name).text in list_of_words:
				if WordListHelper.is_in_list(WordListHelper, vocable.find(words_attribute_name).text, list_of_words, allow_whitespace_characters=True):
					# the vocable was found
					words_added[vocable.find(words_attribute_name).text] = True
					
					# only add attribute value to the vocable, if it doesn't have that value yet
					regex = '\s*' + attribute_value + '\s*$'
					if re.match(regex, vocable.find(attribute_name).text):
						print('Vocable', vocable.find(words_attribute_name).text, 'already has', attribute_value, 'as a', attribute_name, sep=' ', end='\n')
					else:
						#print('adding attribute value ...')
						add_counter += 1
						if vocable.find(attribute_name).text == self.VOCABLE_ATTRIBUTE_VALUE_PLACEHOLDER:
							vocable.find(attribute_name).text = attribute_value
						else:
							vocable.find(attribute_name).text += self.ATTRIBUTE_SEPARATOR + attribute_value
				else:
					#print(vocable.find(words_attribute_name).text, 'is not in list of words', sep=' ', end='\n')
					pass
			
			print('\n')
			print('added', add_counter, attribute_name, 'attribute values to vocables', sep=' ', end='\n')
			print('\n')
			
			missing_vocables_counter = 0
			for key in words_added:
				if not words_added[key]:
					print(key + ' was not found in your vocables file.')
					missing_vocables_counter += 1
			
			print('\n')
			print(missing_vocables_counter, 'vocables were not found in your vocables file.', sep=' ', end='\n')
			print('\n')
			
		except XMLParserException:
			print("Exception occured while parsing the XML file.")