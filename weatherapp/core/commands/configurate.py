import re
import logging
import configparser

from weatherapp.core import config
from weatherapp.core.abstract import Command
from weatherapp.core.exception import ConfigurateCommandError


class Configurate(Command):

	""" Help to configure weather providers.
	"""

	name = 'configurate'
	logger = logging.getLogger(__name__)

	def get_parser(self):
		parser = super().get_parser()
		parser.add_argument('provider', help='Provider name', nargs='?')
		
		return parser

	def run(self, argv):
		""" Run command.
		"""

		params = self.get_parser().parse_args(argv)

		if params.provider:
			provider_name = params.provider
			if provider_name in self.app.providermanager:
				provider_factory = \
					    self.app.providermanager.get(provider_name)
				provider_factory(self.app).configurate()
		else:
			if self.app.options.reset_defaults:
				self.clear_configurate()
				self.app.stdout.write('The configuration file is deleted! \n')
			else:
				self.logging_configuration()

	def logging_configuration(self):
		""" Displays the menu to select the command for configuring logins.
		"""

		menu = {1: 'Configure login level',
		        2: 'Configure logging into a file or in a console',
		        3: 'Configure name of the log file'}

		for key, value in menu.items():
			self.app.stdout.write(f'{key} {value} \n')

		try:
			selected_index = int(input('Please select number: '))
		except (ValueError, IndexError):
			msg = 'Error!'
			if self.app.options.debug:
				self.logger.exception(msg)
			else:
				self.logger.error(msg)
			raise ConfigurateCommandError(
	    	    		 'You have entered the wrong data format!! \n'
	    	    		 'Repeat again, input a number.', 
	    	    		  name1=self.name).action()

		if selected_index in menu:
			if selected_index == 1:
				self.login_level()
			elif selected_index == 2:
				self.logging_file_or_console()
			elif selected_index == 3:
				self.logfile_name()
		else:
			raise ConfigurateCommandError(
	    	    		 'You have entered a' 
	    	    		 'non-existent number in the list!! \n'
	    	    		 'Repeat again, input a number.', 
	    	    		  name1=self.name).action()

	def login_level(self):
		""" Choice logging level.
		"""

		LOG_LEVEL_MAP = {0: 'WARNING', 
		                 1: 'INFO', 
		                 2: 'DEBUG'}

		for key, value in LOG_LEVEL_MAP.items():
			self.app.stdout.write(f'{key}: {value} \n')

		try:
			log_level_choice = int(input('Please select index: '))
		except (ValueError, IndexError):
			msg = 'Error!'
			if self.app.options.debug:
				self.logger.exception(msg)
			else:
				self.logger.error(msg)
			raise ConfigurateCommandError(
	    	    		 'You have entered the wrong data format!! \n'
	    	    		 'Repeat again, input a number.', 
	    	    		  name1=self.name).action()			
		
		if log_level_choice in LOG_LEVEL_MAP:
			log_level = LOG_LEVEL_MAP.get(log_level_choice)
			self.save_log_configuration(log_level=log_level)
		else:
			raise ConfigurateCommandError(
	    	    		 'You have entered a' 
	    	    		 'non-existent number in the list!! \n'
	    	    		 'Repeat again, input a number.', 
	    	    		  name1=self.name).action()

	def save_log_configuration(self, log_level='INFO', log_output='console', 
		                       log_filename='weatherapp.log'):
		""" Save log level, log output and logfile name for application.
		"""

		parser = configparser.ConfigParser()
		config_file = self.get_configuration_file()

		if config_file.exists():
			parser.read(config_file)

		parser['App'] = {'log-level': log_level,
		                 'log-output': log_output,
		                 'log-filename': log_filename}
		with open(config_file, 'w') as configfile:
			parser.write(configfile)

	def logging_file_or_console(self):
		""" Choice logging into a file or console.
		"""

		LOG_OUTPUT_MAP = {1: 'file',
		                  2: 'console'}

		for key, value in LOG_OUTPUT_MAP.items():
			self.app.stdout.write(f'{key}: {value} \n')

		try:
			log_output_choice = int(input('Please select index: '))
		except (ValueError, IndexError):
			msg = 'Error!'
			if self.app.options.debug:
				self.logger.exception(msg)
			else:
				self.logger.error(msg)
			raise ConfigurateCommandError(
	    	    		 'You have entered the wrong data format!! \n'
	    	    		 'Repeat again, input a number.', 
	    	    		  name1=self.name).action()		
		
		if log_output_choice in LOG_OUTPUT_MAP:
			log_output = LOG_OUTPUT_MAP.get(log_output_choice)
			self.save_log_configuration(log_output=log_output)
		else:
			raise ConfigurateCommandError(
	    	    		 'You have entered a' 
	    	    		 'non-existent number in the list!! \n'
	    	    		 'Repeat again, input a number.', 
	    	    		  name1=self.name).action()

	def logfile_name(self):
		""" Input the name of logfile.
		"""

		log_filename = input('Please input the name of log file: \n ')

		sample_log_file = re.compile("[a-z0-9_]*[.]{0,1}[a-z]{3}")
		check = sample_log_file.match(log_filename)

		if check:
			self.save_log_configuration(log_filename=log_filename)
		else:
			self.app.stdout.write('You inputed incorrect name of log file!\n'
	    		                  'Input againe. \n')

		









