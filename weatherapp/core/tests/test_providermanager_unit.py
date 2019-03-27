import unittest

from weatherapp.core.managers import ProviderManager


class DummyCommand:
	name = 'dummy'

class BarCommand:
	name = 'bar'


class ProviderManagerTestCase(unittest.TestCase):

	""" Unit test case for provider manager.
	"""

	def setUp(self):
		self.provider_manager = ProviderManager()

	def test_add(self):
		""" Test add method for provider manager.
		"""

		self.provider_manager.add('dummy', DummyCommand)

		self.assertTrue('dummy' in self.provider_manager._commands)
		self.assertEqual(self.provider_manager.get('dummy'), DummyCommand)

	def test_get(self):
		""" Test application get method.
		"""

		self.provider_manager.add('dummy', DummyCommand)

		self.assertEqual(self.provider_manager.get('dummy'), DummyCommand)
		self.assertIsNone(self.provider_manager.get('bar'))

	def test_contains(self):
		""" Test if '__contains__' method is working.
		"""

		self.provider_manager.add('dummy', DummyCommand)

		self.assertTrue('dummy' in self.provider_manager)
		self.assertFalse('bar' in self.provider_manager)

	def test_len(self):
		""" Test if '__len__' method is working.
		"""

		self.provider_manager.add('dummy', DummyCommand)

		self.assertEqual(self.provider_manager._commands.__len__(), 4)

	def test_getitem(self):
		""" Test if '__getitem__' method is working.
		"""

		self.provider_manager.add('dummy', DummyCommand)

		self.assertEqual(self.provider_manager._commands['dummy'], 
			             DummyCommand)

	def test_iter(self):
		""" Test if '__iter__' method is working.
		"""

		self.provider_manager.add('dummy', DummyCommand)
		self.provider_manager.add('bar', BarCommand)

		for command_name, command in self.provider_manager:
			self.assertTrue('dummy' in self.provider_manager)
			self.assertTrue('bar' in self.provider_manager)

	def test_load_commands(self):
		""" Test application '_load_commands' method.
		"""

		entry_points={'dummy': DummyCommand}
		
		for key, value in entry_points.items():
			self.provider_manager.add(key, value)

		self.assertTrue('dummy' in self.provider_manager)
		self.assertEqual(self.provider_manager._commands.get('dummy'), DummyCommand)
		self.assertFalse('bar' in self.provider_manager)


if __name__ == '__main__':
	unittest.main()
