__author__ = 'xiaolong'


class XMLInvalidException(BaseException):
	def __init__(self, message):
		super(XMLInvalidException, self).__init__(message)