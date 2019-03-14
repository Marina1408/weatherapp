from weatherapp.core.abstract import Command


class ClearCacheDir(Command):

	""" Clear all cache files and the cach directory.
	"""

	name = 'clear_cache'

	def run(self, argv):
		""" Run command.
		"""

		self.clear_all_cache()
		self.app.stdout.write('Clear all cache files. \n')