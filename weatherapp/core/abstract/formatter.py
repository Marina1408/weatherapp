import abc


class Formatter(abc.ABC):
	
	""" Base abstract class for formatters.
	"""

	@abc.abstractmethod
	def emit(self, column_names, data):
		""" Format and print data from the iterable source.

		:param column_names: names of the columns
		:type column_names: list
		:param data: iterable data source, one tuple per object
		             with values in order of column names
		:type data: list or tuple
		"""