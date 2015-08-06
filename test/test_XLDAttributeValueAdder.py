# -*- coding: utf-8 -*-

import re
from test.path_helper import go_up
from xldattributevalueadder.VocableFileWriter import VocableFileWriter
from xldattributevalueadder.WordListHelper import WordListHelper
from xldattributevalueadder.WordListReader import WordListReader
from xldattributevalueadder.XLDAttributeValueAdder import XLDAttributeValueAdder
from xldattributevalueadder.exceptions.XMLInvalidException import XMLInvalidException
from xldattributevalueadder.exceptions.XMLParseException import XMLParserException
from xldattributevalueadder.xmlparser.XMLParser import XMLParser

__author__ = 'xiaolong'

import os
from xml.dom import minidom
from lxml import etree



class TestXLDAttributeValueAdder:
	def setup (self):
		self.test_directory = os.path.dirname(os.path.realpath(__file__)) + '/'
		self.project_directory = go_up(self.test_directory)
		
		vocable_file_path = self.project_directory + 'res/vocables.xml'
		xsd_file_path = self.project_directory + 'res/xld-vocables-schema.xsd'
		word_list_file_path = self.project_directory + 'res/HSK1'
		
		self.attribute_name = 'chapters'
		self.words_attribute_name = 'secondLanguageTranslations'
		self.attribute_value = 'HSK1-2012'
		
		self.attribute_index_to_attribute_name = [
			'firstLanguageTranslations',
			'firstLanguagePhoneticScripts',
			'secondLanguageTranslations',
			'secondLanguagePhoneticScripts',
			'topics',
			'chapters',
			'description',
			'learnLevel',
			'relevanceLevel'
		]
		
		self.test_vocables = [
			['Du','---','你','nǐ','Personalpronomen','PC01 / LSC01 / NPC01','---','5','5'],
			['gut','---','好','hǎo','---','PC01 / LSC01 / NPC01','---','5','---'],
			['---','---','吗','ma','Grammatik/Fragepartikel','PC02/LSC01/NPC01','---','5','---'],
			['ich / mir / mich','---','我','wǒ','Grammatik / Personalpronomen','PC02 / LSC01 / NPC01','---','5','---'],
			['sehr','---','很','hěn','Adjektive','PC02 / LSC01 / NPC01','---','5','---'],
			
			['---','---','呢','ne','Grammatik / Modalpartikel','PC02 / NPC01','---','5','---'],
			['beschaeftigt','---','忙','máng','---','PC03 / NPC02','---','5','---'],
			['nein / nicht','---','不','bù','---','PC03 / LSC01 / NPC02','---','5','---'],
			['aelterer Bruder (der)','---','哥哥','gēge','Familie','PC03 / NPC02','---','5','---'],
			['er / ihm / ihn','---','他','tā','Grammatik / Personalpronomen','PC03 / LSC01 / NPC02','---','5','---']
		]
		
		self.ATTRIBUTE_SEPARATOR = '/'
	
	def teardown (self):
		pass
	
	def setup_class (cls):
		pass
	
	def teardown_class (cls):
		pass
	
	def setup_method (self, method):
		pass
	
	def teardown_method (self, method):
		test_vocable_file_path = self.test_directory + 'test_vocables_file.xml'
		test_word_list_file_path = self.test_directory + 'test_words_list'
		test_list_of_words_file_path = self.test_directory + 'test_list_of_words'
		
		if os.path.isfile(test_vocable_file_path):
			os.remove(test_vocable_file_path)
		if os.path.isfile(test_word_list_file_path):
			os.remove(test_word_list_file_path)
		if os.path.isfile(test_list_of_words_file_path):
			os.remove(test_list_of_words_file_path)
			
	
	def test_is_in_word_list (self):
		fail_message = 'word found or not found in word list although the opposite should be the case'
		allow_whitespace_characters = False
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['a'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['a','b'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b','a'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b','a','c'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'a', ['b','c'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'a', ['b',' a','c'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'a', ['b','a ','c'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'a', ['b',' a ','c'], allow_whitespace_characters), fail_message
		
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['ab'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['b', 'ab'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['ab', 'c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['b', 'ab', 'c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['bd', 'ab', 'c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['b', 'ab', 'cd'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['bd', 'ab', 'cd'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['bde', 'ab', 'cd'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'ab', ['bde', 'cd'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'ab', ['bde', '', 'cd'], allow_whitespace_characters), fail_message
		
		assert WordListHelper.is_in_list(WordListHelper, '我', ['我'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, '你', ['你','b'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, '好', ['b','好'], allow_whitespace_characters), fail_message
		
		allow_whitespace_characters = True
		
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['a'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'A', ['a'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'a', ['A'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['a','b'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b','a'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b','a','c'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'a', ['b','c'], allow_whitespace_characters), fail_message
		# with spaces
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b',' a','c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b','a ','c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b',' a ','c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b','	a','c'], allow_whitespace_characters), fail_message
		# with tabs
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b','a	','c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b','	a','c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b','	a	','c'], allow_whitespace_characters), fail_message
		# with spaces and tabs
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b','	a ','c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'a', ['b',' a	','c'], allow_whitespace_characters), fail_message
		
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['ab'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['b', 'ab'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['ab', 'c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['b', 'ab', 'c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['bd', 'ab', 'c'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['b', 'ab', 'cd'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['bd', 'ab', 'cd'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'ab', ['bde', 'ab', 'cd'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'ab', ['bde', 'cd'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'ab', ['bde', '', 'cd'], allow_whitespace_characters), fail_message
		
		assert WordListHelper.is_in_list(WordListHelper, '我', ['我'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, '你', ['你','b'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, '好', ['b','好'], allow_whitespace_characters), fail_message
		
		assert WordListHelper.is_in_list(WordListHelper, 'Pīnyīn', ['Pīnyīn','好'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'Pīnyīn', ['b','好'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'níhǎoma', ['níhǎoma','好'], allow_whitespace_characters), fail_message
		assert WordListHelper.is_in_list(WordListHelper, 'níhǎoma', ['b','níhǎoma'], allow_whitespace_characters), fail_message
		
		
		assert WordListHelper.is_in_list(WordListHelper, 'níhǎoma', ['test ', 'b','níhǎoma', '?!§', 'an1'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'níhǎoma', ['	test', 'b','1níhǎoma', '?!§', 'an1'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'níhǎoma', ['	test', 'b','níhǎoma3', '?!§', 'an1'], allow_whitespace_characters), fail_message
		assert not WordListHelper.is_in_list(WordListHelper, 'níhǎoma', ['	test', 'b','1níhǎoma2', '?!§', 'an1'], allow_whitespace_characters), fail_message
	
	
	def test_get_list_of_words (self):
		test_file_path = self.test_directory + 'test_list_of_words'
		
		written_words = ['a','A','ab','AB','aB','Ab','níhǎo','Níhǎo','你好']
		with open(test_file_path, 'w') as file:
			for word in written_words:
				file.write(word + '\n')
		
		read_words = WordListReader.read(WordListReader, test_file_path)
		
		"""
		for read_word in read_words:
			assert read_word in written_words, 'found a word which was not written'
		for written_word in written_words:
			assert written_word in read_words, 'A written word was not found in the list of read words.'
		"""
		
		assert len(written_words) == len(read_words), 'The amount of written words is not the same as the amount of read words.'
		assert len(set(written_words).intersection(read_words)) == len(written_words), 'The written words are not all in the list of read words.'
	
	def test_write_vocable_file (self):
		print('current working directory:', os.getcwd())
		
		vocable_file_path = self.create_test_vocables_file()
		print('--- using vocable file path:', vocable_file_path)
		
		list_of_words = ['你','好','吗','我','很']
		words_list_file_path = self.create_test_words_file(list_of_words)
		
		xsd_file_path = self.project_directory + 'res/xld-vocables-schema.xsd'
		
		attribute_name = 'chapters'
		attribute_value = 'HSK1-2012'
		words_attribute_name = 'secondLanguageTranslations'
		
		
		xml_parser = XMLParser()
		xld_attribute_adder = XLDAttributeValueAdder(vocable_file_path, xsd_file_path, words_list_file_path)
		
		xml_root = xml_parser.get_xml_element_tree_root(xsd_file_path, vocable_file_path)
		
		xld_attribute_adder.add_values_to_attribute_of_vocables(attribute_name, attribute_value, words_attribute_name)
		VocableFileWriter.write(VocableFileWriter, xsd_file_path, vocable_file_path, xml_root)
		
		assert os.path.isfile(vocable_file_path), 'no file exists'
		
		# if the xml is not valid anymore when reading the file, the write function might have done something wrong
		try:
			xml_root = xml_parser.get_xml_element_tree_root(xsd_file_path, vocable_file_path)
		except XMLParserException as exception:
			assert False
		else:
			assert True
	
	def test_write_vocable_file_failing (self):
		print('current working directory:', os.getcwd())
		
		vocable_file_path = self.create_test_vocables_file()
		print('--- using vocable file path:', vocable_file_path)
		
		list_of_words = ['你','好','吗','我','很']
		words_list_file_path = self.create_test_words_file(list_of_words)
		
		xsd_file_path = self.project_directory + 'res/xld-vocables-schema.xsd'
		
		attribute_name = 'chapters'
		attribute_value = 'HSK1-2012'
		words_attribute_name = 'secondLanguageTranslations'
		
		
		xml_parser = XMLParser()
		xld_attribute_adder = XLDAttributeValueAdder(vocable_file_path, xsd_file_path, words_list_file_path)
		
		xml_root = xml_parser.get_xml_element_tree_root(xsd_file_path, vocable_file_path)
		
		xld_attribute_adder.add_values_to_attribute_of_vocables(attribute_name, attribute_value, words_attribute_name)
		
		# adding invalid tags with texts
		invalid_vocable_element = etree.SubElement(xml_root, 'vocable')
		abc_element = etree.SubElement(invalid_vocable_element, 'abc')
		abc_element.text = 'abc'
		unknowntag_element = etree.SubElement(invalid_vocable_element, 'unknowntag')
		unknowntag_element.text = 'unknowntag'
		
		# the tree should be invalid at this point
		assert xml_parser.validate_tree(xsd_file_path, xml_root) == False, 'Your validation does not work properly.'
		
		# if the xml is not valid anymore when reading the file, the write function might have done something wrong
		try:
			VocableFileWriter.write(VocableFileWriter, xsd_file_path, vocable_file_path, xml_root)
		except XMLInvalidException as exception:
			assert True
		else:
			assert False
		
		
		assert os.path.isfile(vocable_file_path), 'no file exists'
		
		xml_root = xml_parser.get_xml_element_tree_root(xsd_file_path, vocable_file_path)
	
	
	def create_test_vocables_file (self):
		# create the file
		test_vocables_file_path = self.test_directory + 'test_vocables_file.xml'
		
		try:
			with open(test_vocables_file_path, 'wb') as test_vocables_file:
				# create the xml root element <list>
				vocables_xml_root = etree.Element('list')
				for vocable in self.test_vocables:
					# create a vocable element <vocable>
					vocable_xml = etree.SubElement(vocables_xml_root, 'vocable')
					
					for i in range(len(self.attribute_index_to_attribute_name)):
						# create vocable attribute for example <firstLanguageTranslations>
						attribute = etree.SubElement(vocable_xml, self.attribute_index_to_attribute_name[i])
						attribute.text = vocable[i]
				
				rough_string = etree.tostring(vocables_xml_root, encoding='unicode', xml_declaration=False)
				reparsed = minidom.parseString(rough_string)
				pretty_printed = reparsed.toprettyxml(indent='\t', encoding='utf-8')
				
				test_vocables_file.write(pretty_printed)
		
		except IOError:
			print("Error while writing in log file!")
			
		finally:
			return test_vocables_file_path
	
	
	def create_test_words_file (self, list_of_words):
		test_words_list_file_path = self.test_directory + 'test_words_list'
		with open(test_words_list_file_path, 'w') as words_list_file:
			for word in list_of_words:
				words_list_file.write(word + '\n')
		
		return test_words_list_file_path
	
	
	def test_add_values_to_attribute_of_vocables (self):
		xml_parser = XMLParser()
		
		list_of_words = ['你','好','吗','我','很']
		
		test_word_list_file_path = self.create_test_words_file(list_of_words)
		test_vocable_file_path = self.create_test_vocables_file()
		xsd_file_path = self.project_directory + 'res/xld-vocables-schema.xsd'
		
		# TODO: check if the chapter is not in the vocables already
		# attribute value hasn't been added yet, so it should not already be in the vocables
		# this assertion is necessary to check if the add_values_to_attribute_of_vocables really changes something
		xml_root = xml_parser.get_xml_element_tree_root(xsd_file_path, test_vocable_file_path)
		
		for vocable in xml_root:
			vocable_word_attribute_text = vocable.find(self.words_attribute_name).text
			# is this vocable one of the world list?
			if WordListHelper.is_in_list(WordListHelper, vocable_word_attribute_text, list_of_words, allow_whitespace_characters=True):
				print(vocable_word_attribute_text, 'is in word list')
				attribute_text = vocable.find(self.attribute_name).text
				# does this vocable have the added attribute value?
				regex = '^.*'+re.escape(self.ATTRIBUTE_SEPARATOR) + self.attribute_value + re.escape(self.ATTRIBUTE_SEPARATOR)+'.*$'
				print('regex:', regex)
				print('attribute_text:', attribute_text)
				assert re.match(regex, attribute_text) is None, 'attribute value has already added to vocable ' + vocable.find(self.words_attribute_name).text
		
		
		# now add the attribute value
		xld_attribute_adder = XLDAttributeValueAdder(test_vocable_file_path, xsd_file_path, test_word_list_file_path)
		xld_attribute_adder.add_values_to_attribute_of_vocables(self.attribute_name, self.attribute_value, self.words_attribute_name)
		VocableFileWriter.write(VocableFileWriter, xsd_file_path, test_vocable_file_path, xld_attribute_adder.xml_root)
		
		
		# check the vocables again, to see if something has been added
		xml_root = xml_parser.get_xml_element_tree_root(xsd_file_path, test_vocable_file_path)
		
		for vocable in xml_root:
			vocable_word_attribute_text = vocable.find(self.words_attribute_name).text
			# is this vocable one of the world list?
			if WordListHelper.is_in_list(WordListHelper, vocable_word_attribute_text, list_of_words, allow_whitespace_characters=True):
				print(vocable_word_attribute_text, 'is in word list')
				attribute_text = vocable.find(self.attribute_name).text
				# does this vocable have the added attribute value?
				regex = r'\s*' + self.attribute_value + r'\s*$'
				print('regex:', regex)
				print('attribute_text:', attribute_text)
				assert re.search(regex, attribute_text) is not None, 'attribute value has not been added to vocable ' + vocable.find(self.words_attribute_name).text