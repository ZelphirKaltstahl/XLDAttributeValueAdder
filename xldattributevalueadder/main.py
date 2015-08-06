#!/home/xiaolong/Development/Anaconda3/envs/xld-attribute-value-adder/bin/python3.4
# -*- coding: utf-8 -*-

import os
import sys
from xldattributevalueadder.VocableFileWriter import VocableFileWriter
from xldattributevalueadder.XLDAttributeValueAdder import XLDAttributeValueAdder

__author__ = 'xiaolong'

def main():
	'''
	project_directory = os.path.dirname(os.path.realpath(__file__)) + '/'
	sys.path.append(project_directory)
	for p in sys.path:
		print(p)
	'''
	vocable_file_path = input('Vocable file path:')
	xsd_file_path = input('XSD file path:')
	words_file_path = input('Word list file path:')
	
	attribute_name = input('Attribute name:')
	words_attribute_name = input('Words attribute name:')
	attribute_value = input('Attribute value:')
	
	if vocable_file_path == '': vocable_file_path = '/home/xiaolong/Development/PycharmProjects/xld-attribute-value-adder/res/vocables.xml'
	if xsd_file_path == '': xsd_file_path = '/home/xiaolong/Development/PycharmProjects/xld-attribute-value-adder/res/xld-vocables-schema.xsd'
	if words_file_path == '': words_file_path = '/home/xiaolong/Development/PycharmProjects/xld-attribute-value-adder/res/HSK2'
	if attribute_name == '': attribute_name = 'chapters'
	if words_attribute_name == '': words_attribute_name = 'secondLanguageTranslations'
	if attribute_value == '': attribute_value = 'HSK2-2012'
	
	print('inputs received:\n')
	print('vocable file path: ', vocable_file_path, sep=' ', end='\n')
	print('xsd file path: ', xsd_file_path, sep=' ', end='\n')
	print('words file path: ', words_file_path, sep=' ', end='\n')
	print('attribute name: ', attribute_name, sep=' ', end='\n')
	print('words attribute name: ', words_attribute_name, sep=' ', end='\n')
	print('attribute_value: ', attribute_value, sep=' ', end='\n')
	
	xld_attribute_adder = XLDAttributeValueAdder(vocable_file_path, xsd_file_path, words_file_path)
	
	xld_attribute_adder.add_values_to_attribute_of_vocables(attribute_name, attribute_value, words_attribute_name)
	VocableFileWriter.write(VocableFileWriter, xsd_file_path, vocable_file_path, xld_attribute_adder.xml_root)
	
	input('\nThe new vocable file is written. Press [Enter] to exit.')
	
if __name__ == '__main__':
	main()