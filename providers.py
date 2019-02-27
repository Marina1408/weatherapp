import re
import urllib.parse

from bs4 import BeautifulSoup

import config
import decorators
from abstract import WeatherProvider


class AccuWeatherProvider(WeatherProvider):

	""" Weather provider for AccuWeather site.
	"""

	name = config.ACCU_PROVIDER_NAME
	title = config.ACCU_PROVIDER_TITLE

	def get_name(self):
		return self.name

	def get_default_location(self):
		""" Default location name.
		"""

		return config.DEFAULT_ACCU_LOCATION_NAME

	def get_default_url(self):
		""" Default location url.
		"""

		return config.DEFAULT_ACCU_LOCATION_URL

	def get_locations_accu(self, locations_url):
	    """ Getting locations from accuweather.
	    """

	    locations_page = self.get_page_source(locations_url)
	    soup = BeautifulSoup(locations_page, 'html.parser')

	    locations = []
	    for location in soup.find_all('li', class_='drilldown cl'):
	    	url = location.find('a').attrs['href']
	    	location = location.find('em').text
	    	locations.append((location, url))
	    return locations

	def configurate(self):
	    """ Displays the list of locations for the user to select from 
	        AccuWeather.
	    """

	    locations = self.get_locations_accu(config.ACCU_BROWSE_LOCATIONS)
	    while locations:
	    	for index, location in enumerate(locations):
	    		print(f'{index + 1}. {location[0]}')

	    	try:
	    		selected_index = int(input('Please select location: '))
	    	except ValueError:
	    		print('You have entered the wrong data format! \n'
	    			  'Repeat againe, input a number.')
	    		break

	    	try:
	    		location = locations[selected_index - 1]
	    	except IndexError:
	    		print('You have entered a non-existent number in the list! \n'
	    			  'Repeat againe.')
	    		break

	    	locations = self.get_locations_accu(location[1])

	    self.save_configuration(*location)

	def get_weather_info(self, page_content):
	    """ Getting the final result in tuple from site accuweather.
	    """

	    city_page = BeautifulSoup(page_content, 'html.parser')
	    weather_info = {}
	    if not self.app.options.tomorrow:
	    	current_day_selection = city_page.find\
	    	         ('li', class_=re.compile('(day|night) current first cl'))
	    	if current_day_selection:
	    		current_day_url = \
	    		                current_day_selection.find('a').attrs['href']
	    		if current_day_url:
	    			current_day_page = self.get_page_source(current_day_url)
	    			if current_day_page:
	    				current_day = BeautifulSoup(current_day_page,
                                                    'html.parser')
	    				weather_details = current_day.find('div',
                                                   attrs={'id': 'detail-now'})
	    				condition = weather_details.find('span', 
	    					                             class_='cond')
	    				if condition:
	    					weather_info['cond'] = condition.text
	    				temp = weather_details.find('span', 
	    					                         class_='large-temp')
	    				if temp:
	    					weather_info['temp'] = temp.text
	    				feal_temp = weather_details.find(
                            'span', class_='small-temp')
	    				if feal_temp:
	    					weather_info['feal_temp'] = feal_temp.text
	    else:
	    	tomorrow_day_selection = city_page.find('li',
                                                    class_='day last hv cl')
	    	if tomorrow_day_selection:
	    		tomorrow_day_url = \
	    		                tomorrow_day_selection.find('a').attrs['href']
	    		if tomorrow_day_url:
	    			tomorrow_day_page = self.get_page_source(tomorrow_day_url)
	    			if tomorrow_day_page:
	    				tomorrow_day = BeautifulSoup(tomorrow_day_page,
                                                     'html.parser')
	    				weather_details = tomorrow_day.find('div',
                                             attrs={'id': 'detail-day-night'})
	    				condition = weather_details.find('div', class_='cond')
	    				if condition:
	    					weather_info['cond'] = condition.text.strip()
	    				temp = weather_details.find('span', 
	    					                         class_='large-temp')
	    				if temp:
	    					weather_info['temp'] = temp.text
	    				feal_temp = weather_details.find('span', 
                                                         class_='realfeel')
	    				if feal_temp:
	    					weather_info['feal_temp'] = feal_temp.text

	    return weather_info


class Rp5WeatherProvider(WeatherProvider):

	""" Weather provider for RP5 site.
	"""

	name = config.RP5_PROVIDER_NAME
	title = config.RP5_PROVIDER_TITLE

	def get_name(self):
		return self.name

	def get_default_location(self):
		""" Default location name.
		"""

		return config.DEFAULT_RP5_LOCATION_NAME

	def get_default_url(self):
		""" Default location url.
		"""

		return config.DEFAULT_RP5_LOCATION_URL

	def get_locations_rp5(self, locations_url):
	    """ Getting locations from rp5.ua.
	    """

	    locations_page = self.get_page_source(locations_url)
	    soup = BeautifulSoup(locations_page, 'html.parser')
	    part_url = ''

	    locations = []
	    for location in soup.find_all('div', class_='country_map_links'):
	    	part_url = location.find('a').attrs['href']
	    	part_url = urllib.parse.quote(part_url)
	    	url = config.base_url_rp5 + part_url
	    	location = location.find('a').text
	    	locations.append((location, url))
	    if locations == []:
	    	for location in soup.find_all('h3'):
	    		part_url = location.find('a').attrs['href']
	    		part_url = urllib.parse.quote(part_url)
	    		url = config.base_url_rp5 + '/' + part_url
	    		location = location.find('a').text
	    		locations.append((location, url))

	    return locations

	def configurate(self):
	    """ Displays the list of locations for the user to select from RP5.
	    """

	    locations = self.get_locations_rp5(config.RP5_BROWSE_LOCATIONS)
	    while locations:
	    	for index, location in enumerate(locations):
	    		print(f'{index + 1}. {location[0]}')

	    	try:
	    		selected_index = int(input('Please select location: '))
	    	except (UnboundLocalError, ValueError):
	    		print('You have entered the wrong data format! \n'
	    			  'Repeat againe, input a number.')
	    		break

	    	try:
	    		location = locations[selected_index - 1]
	    	except IndexError:
	    		print('You have entered a non-existent number in the list! \n'
	    			  'Repeat againe.')
	    		break

	    	locations = self.get_locations_rp5(location[1])

	    self.save_configuration(*location)

	@decorators.timer
	def get_weather_info(self, page_content):
	    """ Getting the final result in tuple from site rp5.
	    """

	    city_page = BeautifulSoup(page_content, 'html.parser')
	    weather_info = {}
	    if not self.app.options.tomorrow:
	    	weather_details = city_page.find('div', 
	    		                      attrs={'id': 'archiveString'})
	    	weather_details_cond = weather_details.find('div', 
	    		                                   class_='ArchiveInfo')
	    	conditions = weather_details.get_text()
	    	condition = str(conditions[conditions.find('F,')+3:])
	    	if condition:
	    		weather_info['cond'] = condition
	    	weather_details_temp = weather_details.find('div',
                                                    class_='ArchiveTemp')
	    	temp = weather_details_temp.find('span', class_='t_0')
	    	if temp:
	    		weather_info['temp'] = temp.text
	    	weather_details_feal_temp = weather_details.find('div',
                                                class_='ArchiveTempFeeling')
	    	feal_temp = weather_details_feal_temp.find('span', class_='t_0')
	    	if feal_temp:
	    		weather_info['feal_temp'] = feal_temp.text
	    else:
	    	weather_details = city_page.find('div', attrs={'id': 
                                                   'forecastShort-content'})
	    	weather_details_tomorrow = weather_details.find('span',
                                                        class_='second-part')
	    	conditions = weather_details_tomorrow.findPrevious('b').text
	    	condition_all = str(conditions[conditions.find('Завтра:')+28:])
	    	condition = str(condition_all[condition_all.find('F,')+3:])
	    	if condition:
	    		weather_info['cond'] = condition
	    	temp = weather_details_tomorrow.find('span', class_='t_0')
	    	if temp:
	    		weather_info['temp'] = temp.text

	    return weather_info


class SinoptikWeatherProvider(WeatherProvider):

	""" Weather provider for Sinoptik.ua site.
	"""

	name = config.SINOPTIK_PROVIDER_NAME
	title = config.SINOPTIK_PROVIDER_TITLE

	def get_name(self):
		return self.name

	def get_default_location(self):
		""" Default location name.
		"""

		return config.DEFAULT_SINOPTIK_LOCATION_NAME

	def get_default_url(self):
		""" Default location url.
		""" 
		return config.DEFAULT_SINOPTIK_LOCATION_URL

	def configurate(self):
	    """ Asking the user to input the city.
	    """

	    base_url = 'https://ua.sinoptik.ua'
	    part_1_url = '/погода-'
	    part_1_url = urllib.parse.quote(part_1_url)

	    location = input('Введіть назву міста кирилицею: \n').lower()
	    sample_location = re.compile('[А-яіЇЄє-]*')
	    check = sample_location.match(location)

	    if check.group(0) == location:
	    	part_2_url = urllib.parse.quote(location)
	    	url = base_url + part_1_url + part_2_url
	    	self.save_configuration(location, url)
	    else:
	    	print('You inputed incorrect location! \nInput againe.')

	    part_2_url = urllib.parse.quote(location)
	    url = base_url + part_1_url + part_2_url

	    self.save_configuration(location, url)
	    
	@decorators.timer
	def get_weather_info(self, page_content):
	    """ Getting the final result in tuple from sinoptik.ua site.
	    """

	    city_page = BeautifulSoup(page_content, 'html.parser')
	    weather_info = {}
	    weather_details = city_page.find('div', class_='tabsContent')
	    if not self.app.options.tomorrow:
	    	weather_details = city_page.find('div', class_='tabsContent')
	    	condition_weather_details = weather_details.find('div', 
                                      class_='wDescription clearfix')
	    	condition = condition_weather_details.find('div', 
                                                class_='description')
	    	if condition:
	    		weather_info['cond'] = condition.text.strip()
	    	temp = weather_details.find('p', class_='today-temp')
	    	if temp:
	    		weather_info['temp'] = temp.text
	    	weather_details_feal_temp = weather_details.find('tr',
                                        class_='temperatureSens')
	    	feal_temp = weather_details_feal_temp.find('td', 
	    		          class_=re.compile(
                          '(p5 cur)|(p1)|(p2 bR)|(p3)|(p4 bR)|(p5)|(p6 bR)|'
                          '(p7 cur)|(p8)'))
	    	if feal_temp:
	    		weather_info['feal_temp'] = feal_temp.text
	    else:
	    	weather_details = city_page.find('div', attrs={'id': 'bd2'})
	    	temp = weather_details.find('div', class_='max')
	    	if temp:
	    		weather_info['temp'] = temp.text
	    	feal_temp = weather_details.find('div', class_='min')
	    	if feal_temp:
	    		weather_info['feal_temp'] = feal_temp.text
	    	tomorrow_day_selection = city_page.find('div',
                                             attrs={'id': 'bd2'})
	    	if tomorrow_day_selection:
	    		part_url = tomorrow_day_selection.find('a').attrs['href']
	    		part_url = urllib.parse.quote(part_url)
	    		base_url = 'http:' 
	    		tomorrow_day_url = base_url + part_url
	    		if tomorrow_day_url:
	    			tomorrow_day_page = self.get_page_source(tomorrow_day_url)
	    			if tomorrow_day_page:
	    				tomorrow_day = BeautifulSoup(tomorrow_day_page,
                                                 'html.parser')
	    				weather_details = tomorrow_day.find('div',
                                             class_='wDescription clearfix')
	    				condition = weather_details.find('div', 
                                                     class_='description')
	    				if condition:
	    					weather_info['cond'] = condition.text.strip()

	    return weather_info

	






























