import pytest as pytest

__author__ = 'xiaolong'

class TestTemplate:
	def setup(self):
		pass

	def teardown(self):
		pass
	
	def setup_class(cls):
		pass
		
	def teardown_class(cls):
		pass

	def setup_method(self, method):
		pass

	def teardown_method(self, method):
		pass
	
	
	@pytest.fixture()
	def method_name_1(self):
		c = 2
		pass
	
	@pytest.mark.usefixtures('method_name_1')
	def method_name_2(self):
		a = 2
		b = 2
		assertion_fail_message = 'Your computer can\'t compare two numbers.'
		assert a == b, assertion_fail_message
	
	