import unittest

from weatherapp.core.managers import FormatterManager


class DummyCommand:
	name = 'dummy'

class BarCommand:
	name = 'bar'


class FormatterManagerTestCase(unittest.TestCase):

	""" Unit test case for formatter manager.
	"""

	def setUp(self):
		self.formatter_manager = FormatterManager()

	def test_add(self):
		""" Test add method for formatter manager.
		"""

		self.formatter_manager.add('dummy', DummyCommand)

		self.assertTrue('dummy' in self.formatter_manager._commands)
		self.assertEqual(self.formatter_manager.get('dummy'), DummyCommand)

	def test_get(self):
		""" Test application get method.
		"""

		self.formatter_manager.add('dummy', DummyCommand)

		self.assertEqual(self.formatter_manager.get('dummy'), DummyCommand)
		self.assertIsNone(self.formatter_manager.get('bar'))

	def test_contains(self):
		""" Test if '__contains__' method is working.
		"""

		self.formatter_manager.add('dummy', DummyCommand)

		self.assertTrue('dummy' in self.formatter_manager)
		self.assertFalse('bar' in self.formatter_manager)

	def test_len(self):
		""" Test if '__len__' method is working.
		"""

		self.formatter_manager.add('dummy', DummyCommand)

		self.assertEqual(self.formatter_manager._commands.__len__(), 4)

	def test_getitem(self):
		""" Test if '__getitem__' method is working.
		"""

		self.formatter_manager.add('dummy', DummyCommand)

		self.assertEqual(self.formatter_manager._commands['dummy'], 
			             DummyCommand)

	def test_iter(self):
		""" Test if '__iter__' method is working.
		"""

		self.formatter_manager.add('dummy', DummyCommand)
		self.formatter_manager.add('bar', BarCommand)

		for command_name, command in self.formatter_manager:
			self.assertTrue('dummy' in self.formatter_manager)
			self.assertTrue('bar' in self.formatter_manager)

	def test_load_commands(self):
		""" Test application '_load_commands' method.
		""" 

		for command in [DummyCommand, BarCommand]:
		    self.formatter_manager.add(command.name, command)

		self.assertTrue('dummy' in self.formatter_manager._commands)
		self.assertEqual(self.formatter_manager.get('dummy'), DummyCommand)
		self.assertTrue('bar' in self.formatter_manager._commands)
		self.assertEqual(self.formatter_manager.get('bar'), BarCommand)


if __name__ == '__main__':
	unittest.main()

