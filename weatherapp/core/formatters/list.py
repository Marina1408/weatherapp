from weatherapp.core.abstract import Formatter


class ListFormatter(Formatter):

 	""" List formatter for app output.
 	"""

 	def emit(self, columns, data):
	    """ Displays the final result of the program
	    """

	    title = columns[0]
	    location = columns[1]

	    a = title + '\n' + "*"*12 + '\n' + location + '\n' + '-'*12 
	    b = []

	    for key, value in data.items():
	    	c = str(f'{key} : {value}')
	    	b.append(c)

	    b = str(b)
	    return a + '\n' + b + '\n'
	   
	    
	    
	    


	    
	    
	   
	    