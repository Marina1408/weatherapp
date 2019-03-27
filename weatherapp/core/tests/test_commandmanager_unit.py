import unittest

from weatherapp.core.managers import CommandManager


class DummyCommand:
	name = 'dummy'

class BarCommand:
	name = 'bar'


class CommandManagerTestCase(unittest.TestCase):

	""" Unit test case for command manager.
	"""

	def setUp(self):
		self.command_manager = CommandManager()

	def test_add(self):
		""" Test add method for command manager.
		"""

		self.command_manager.add('dummy', DummyCommand)

		self.assertTrue('dummy' in self.command_manager._commands)
		self.assertEqual(self.command_manager.get('dummy'), DummyCommand)

	def test_get(self):
		""" Test application get method.
		"""

		self.command_manager.add('dummy', DummyCommand)

		self.assertEqual(self.command_manager.get('dummy'), DummyCommand)
		self.assertIsNone(self.command_manager.get('bar'))

	def test_contains(self):
		""" Test if '__contains__' method is working.
		"""

		self.command_manager.add('dummy', DummyCommand)

		self.assertTrue('dummy' in self.command_manager)
		self.assertFalse('bar' in self.command_manager)

	def test_len(self):
		""" Test if '__len__' method is working.
		"""

		self.command_manager.add('dummy', DummyCommand)

		self.assertEqual(self.command_manager._commands.__len__(), 4)

	def test_getitem(self):
		""" Test if '__getitem__' method is working.
		"""

		self.command_manager.add('dummy', DummyCommand)

		self.assertEqual(self.command_manager._commands['dummy'], 
			             DummyCommand)

	def test_iter(self):
		""" Test if '__iter__' method is working.
		"""

		self.command_manager.add('dummy', DummyCommand)
		self.command_manager.add('bar', BarCommand)

		for command_name, command in self.command_manager:
			self.assertTrue('dummy' in self.command_manager)
			self.assertTrue('bar' in self.command_manager)

	def test_load_commands(self):
		""" Test application '_load_commands' method.
		""" 

		for command in [DummyCommand, BarCommand]:
		    self.command_manager.add(command.name, command)

		self.assertTrue('dummy' in self.command_manager._commands)
		self.assertEqual(self.command_manager.get('dummy'), DummyCommand)
		self.assertTrue('bar' in self.command_manager._commands)
		self.assertEqual(self.command_manager.get('bar'), BarCommand)



if __name__ == '__main__':
	unittest.main()


