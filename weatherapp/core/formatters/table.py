import prettytable
from argparse import ArgumentParser

from weatherapp.core.abstract import Formatter


class TableFormatter(Formatter):

    """ Table formatter for app output.
    """


    name = 'table'

    def get_parser(self):
        parser = ArgumentParser()
        parser.add_argument('-align', action='store',
                        default='l',
                        help='Align text in the table, defaults to left')
        parser.add_argument('-padding_width', action='store',
                        default=1, type = int,
                        help='Adding the indent in the table, defaults to 1')
        parser.add_argument('-hrules', action='store',
                    default=0, type = int,
                    help='Split horizontally columns in the table, defaults to 0')
        parser.add_argument('--vrules', action='store',
                    default=2, type = int,
                    help='Split vertically columns in the table, defaults to 1')
        return parser

    def emit(self, column_names, data, argv):
        """ Format and print data from the iterable source.

        :param column_names: names of the columns
        :type column_names: list
        :param data: iterable data source, one tuple per object
                     with values in order of column names
        :type data: list or tuple
        :param argv: remaining_args from parser
        :type argv: str or int
        """

        pt = prettytable.PrettyTable()

        for column, values in zip(column_names, (data.keys(), data.values())):
        	if any(values):
        		pt.add_column(column, list(values))

        params = self.get_parser().parse_args(argv)

        if params.align:
            pt.align = params.align
        

        if params.padding_width:
            pt.padding_width = params.padding_width
       

        if params.hrules:
            pt.hrules = params.hrules
       

        if params.vrules:
            pt.vrules = params.vrules
       

        return pt.get_string()


