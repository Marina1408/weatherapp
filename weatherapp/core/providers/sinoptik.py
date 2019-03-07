import re
import urllib.parse

from bs4 import BeautifulSoup

from weatherapp.core import config
from weatherapp.core import decorators
from weatherapp.core.abstract import WeatherProvider


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
	    sample_location = re.compile("[а-яіїє-]*")
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

	

