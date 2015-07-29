import re

__author__ = 'xiaolong'

class WordListHelper():
	
	ATTRIBUTE_SEPARATOR = '/'
	
	def __init__(self):
		pass
	
	@staticmethod
	def is_in_list(self, vocable_attribute_text, list_of_words, allow_whitespace_characters=True):
		""" This method checks if a vocable attribute has a value, which is in a given list of words. """
		vocable_attribute_values = vocable_attribute_text.split(self.ATTRIBUTE_SEPARATOR, maxsplit=-1)
		
		for vocable_attribute_value in vocable_attribute_values:
			return WordListHelper.is_vocable_attribute_value_in_word_list(WordListHelper, vocable_attribute_value, list_of_words, allow_whitespace_characters)
		return False
	
	@staticmethod
	def is_vocable_attribute_value_in_word_list(self, vocable_attribute_value, list_of_words, allow_whitespace_characters=True):
		if allow_whitespace_characters:
			regex = '^\s*' + vocable_attribute_value + '\s*$'
			for word in list_of_words:
				if re.search(regex, word):
					return True
		else:
			for word in list_of_words:
				if vocable_attribute_value == word:
					return True
		
		return False