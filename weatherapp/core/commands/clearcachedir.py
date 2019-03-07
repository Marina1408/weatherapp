from weatherapp.core.abstract import Command


class ClearCacheDir(Command):

	""" Clear all cache files and the cach directory.
	"""

	name = 'clear_cache'

	def run(self, argv):
		""" Run command.
		"""

		self.clear_all_cache()
		print('Clear all cache files.')