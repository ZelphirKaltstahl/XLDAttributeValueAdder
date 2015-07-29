__author__ = 'xiaolong'

class WordListReader():
	
	def __init__(self):
		pass
	
	@staticmethod
	def read(self, word_list_file_path):
		#print('getting list of words from file ...')
		list_of_words = []
		
		with open(word_list_file_path, 'r') as file:
			for line in file:
				list_of_words.append(line.strip('\n'))
		
		return list_of_words
		