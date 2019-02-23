import abstract

from commands import Configurate, Providers, ClearCacheDir


class CommandManager(abstract.Manager):
	""" Manager for app commands.
	"""

	def __init__(self):
		self._commands = {}
		self._load_commands()

	def _load_commands(self):
		""" Loads all external (from an entrypoints)commands.
		"""

		for command in [Configurate, Providers, ClearCacheDir]:
		    self.add(command.name, command)

	def add(self, name, command):
		""" Registers command under specified name.

		:param name:     command name
		:type name:      str
		:param command:  command class
		:type command:   abstract.Command
		"""

		self._commands[name] = command

	def get(self, name):
		""" Get provider by name.
		"""

		return self._commands.get(name, None)

	def __len__(self):
		return len(self._commands)

	def __contains__(self, name):
		return name in self._commands

	def __getitem__(self, name):
		return self._commands[name]