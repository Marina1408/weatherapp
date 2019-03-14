from weatherapp.core.abstract import Formatter


class CsvFormatter(Formatter):

    """ CSV formatter for app output.
    """


    name = 'csv'

    def emit(self, columns, data, argv):
        """ Format and print data from the iterable source.

        :param columns: names of the columns
        :type columns: list
        :param data: iterable data source, one tuple per object
                     with values in order of column names
        :type data: list or tuple
        :param argv: remaining_args from parser
        :type argv: str or int
        """

        title = columns[0]
        location = columns[1]

        a = ' ' + title + ',' + location  
        b = []

        for key, value in data.items():
        	if ' ' in value:
        		value = '"' + value + '"'
        	c = str(key + ',' + value)
        	b.append(c)

        b = str(b)
        b = b.replace("',", "'\n")
        b = b.replace("[", ' ')
        b = b.replace("]", '')
        b = b.replace("'", '')
        return a + '\n' + b + '\n'
       
