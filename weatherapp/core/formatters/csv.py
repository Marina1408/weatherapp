from weatherapp.core.abstract import Formatter


class CsvFormatter(Formatter):

    """ CSV formatter for app output.
    """

    def emit(self, columns, data):
        """ Format and print data from the iterable source.

        :param column_names: names of the columns
        :type column_names: list
        :param data: iterable data source, one tuple per object
                     with values in order of column names
        :type data: list or tuple
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
       
