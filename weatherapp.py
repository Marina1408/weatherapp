#!/usr/bin/env python

""" Weather add project from accuweather, rp5 and sinoptik.ua
"""

import sys
import html
import argparse
import configparser
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


ACCU_URL = ('https://www.accuweather.com/uk/ua/rivne/325590/'
            'weather-forecast/325590')
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'
RP5_BROWSE_LOCATIONS = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0'
                        '%B0_%D0%B2_%D1%81%D0%B2%D1%96%D1%82%D1%96')
SINOPTIK_BROWSE_LOCATIONS = 'https://ua.sinoptik.ua/'

DEFAULT_NAME = 'Kyiv'
DEFAULT_URL_ACCU = ('https://www.accuweather.com/uk/ua/kyiv/324505/'
                    'weather-forecast/324505')
DEFAULT_URL_RP5 = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%'
                   'D0%B2_%D0%9A%D0%B8%D1%94%D0%B2%D1%96')
DEFAULT_URL_SINOPTIK = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%'
                        'D0%B4%D0%B0-%D0%BA%D0%B8%D1%97%D0%B2')

CONFIG_LOCATION = 'location'
CONFIG_FILE_ACCU = 'accu_weatherapp.ini'
CONFIG_FILE_RP5 = 'rp5_weatherapp.ini'
CONFIG_FILE_SINOPTIK = 'sinoptik_weatherapp.ini'
CONFIG_FOLDER = 'weatherapp_ini'


def get_request_headers():
    """Getting headers of the request.
    """

    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}


def get_page_source(url):
    """ Getting page from server.
    """

    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')


def get_locations_accu(locations_url):
    """ Getting locations from accuweather.
    """

    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'html.parser')

    locations = []
    for location in soup.find_all('li', class_='drilldown cl'):
        url = location.find('a').attrs['href']
        location = location.find('em').text
        locations.append((location, url))
    return locations


def get_locations_rp5(locations_url):
    """ Getting locations from rp5.ua.
    """

    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'html.parser')
    base_url = 'http://rp5.ua'
    part_url = ''

    locations = []
    for location in soup.find_all('div', class_='country_map_links'):
        part_url = location.find('a').attrs['href']
        part_url = urllib.parse.quote(part_url)
        url = base_url + part_url
        location = location.find('a').text
        locations.append((location, url))
    if locations == []:
        for location in soup.find_all('h3'):
            part_url = location.find('a').attrs['href']
            part_url = urllib.parse.quote(part_url)
            url = base_url + '/' + part_url
            location = location.find('a').text
            locations.append((location, url))
              
    return locations
    

def get_configuration_file_accu():
    """ Path to configuration file.
    """

    return Path.home() / CONFIG_FOLDER / CONFIG_FILE_ACCU


def get_configuration_file_rp5():
    """ Path to configuration file.
    """
    
    return Path.home() / CONFIG_FOLDER / CONFIG_FILE_RP5


def get_configuration_file_sinoptik():
    """ Path to configuration file.
    """

    return Path.home() / CONFIG_FOLDER / CONFIG_FILE_SINOPTIK


def save_configuration_accu(name, url):
    """ Save selected location in AccuWeather site to configuration file.
    """

    parser = configparser.ConfigParser()
    parser[CONFIG_LOCATION] = {'name': name, 'url': url}
    with open(get_configuration_file_accu(), 'w', 
              encoding='utf-8') as configfile:
        parser.write(configfile)


def save_configuration_rp5(name, url):
    """ Save selected location in RP5.ua site to configuration file.
    """

    parser = configparser.ConfigParser(interpolation=None)
    parser[CONFIG_LOCATION] = {'name': name, 'url': url}
    with open(get_configuration_file_rp5(), 'w', 
              encoding='utf-8') as configfile:
        parser.write(configfile)


def save_configuration_sinoptik(name, url):
    """ Save selected location in ASinoptik.ua site to configuration file.
    """

    parser = configparser.ConfigParser(interpolation=None)
    parser[CONFIG_LOCATION] = {'name': name, 'url': url}
    with open(get_configuration_file_sinoptik(), 'w', 
                                    encoding='utf-8') as configfile:
        parser.write(configfile)


def get_configuration_accu():

    name = DEFAULT_NAME
    url = DEFAULT_URL_ACCU
    parser = configparser.ConfigParser()
    parser.read(get_configuration_file_accu())

    if CONFIG_LOCATION in parser.sections():
        config = parser[CONFIG_LOCATION]
        name, url = config['name'], config['url']
    return name, url


def get_configuration_rp5():

    name = DEFAULT_NAME
    url = DEFAULT_URL_RP5
    parser = configparser.ConfigParser(interpolation=None)
    parser.read(get_configuration_file_rp5(), encoding='utf-8')

    if CONFIG_LOCATION in parser.sections():
        config = parser[CONFIG_LOCATION]
        name, url = config['name'], config['url']
    return name, url


def get_configuration_sinoptik():

    name = DEFAULT_NAME
    url = DEFAULT_URL_SINOPTIK
    parser = configparser.ConfigParser(interpolation=None)
    parser.read(get_configuration_file_sinoptik())

    if CONFIG_LOCATION in parser.sections():
        config = parser[CONFIG_LOCATION]
        name, url = config['name'], config['url']
    return name, url


def configurate_accu():
    """ Displays the list of locations for the user to select
        from AccuWeather.
    """

    locations = get_locations_accu(ACCU_BROWSE_LOCATIONS)
    while locations:
        for index, location in enumerate(locations):
            print(f'{index + 1}. {location[0]}')
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        locations = get_locations_accu(location[1])

    save_configuration_accu(*location)


def configurate_rp5():
    """ Displays the list of locations for the user to select
        from RP5.ua.
    """

    locations = get_locations_rp5(RP5_BROWSE_LOCATIONS)
    while locations:
        for index, location in enumerate(locations):
            print(f'{index + 1}. {location[0]}')
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        locations = get_locations_rp5(location[1])

    save_configuration_rp5(*location)


def configurate_sinoptik():
    """ Asking the user to input the city.
    """
  
    base_url = 'https://ua.sinoptik.ua'
    part_1_url = '/погода-'
    part_1_url = urllib.parse.quote(part_1_url)
    location = input('Введіть назву міста: \n')
    part_2_url = urllib.parse.quote(location)
    url = base_url + part_1_url + part_2_url

    save_configuration_sinoptik(location, url)


def get_weather_info_accu(page_content, tomorrow=False):
    """ Getting the final result in tuple from site accuweather.
    """

    city_page = BeautifulSoup(page_content, 'html.parser')
    weather_info = {}
    if not tomorrow:
        current_day_selection = city_page.find\
                      ('li', class_='day current first cl') or city_page.find\
                      ('li', class_='night current first cl')
        if current_day_selection:
            current_day_url = current_day_selection.find('a').attrs['href']
            if current_day_url:
                current_day_page = get_page_source(current_day_url)
                if current_day_page:
                    current_day = BeautifulSoup(current_day_page,
                                                'html.parser')
                    weather_details = current_day.find('div',
                                                  attrs={'id': 'detail-now'})
                    condition = weather_details.find('span', class_='cond')
                    if condition:
                        weather_info['cond'] = condition.text
                    temp = weather_details.find('span', class_='large-temp')
                    if temp:
                        weather_info['temp'] = temp.text
                    feal_temp = weather_details.find(
                        'span', class_='small-temp')
                    if feal_temp:
                        weather_info['feal_temp'] = feal_temp.text
    else:
        tomorrow_day_selection = city_page.find('li',
                                                class_='day hv cl')
        if tomorrow_day_selection:
            tomorrow_day_url = tomorrow_day_selection.find('a').attrs['href']
            if tomorrow_day_url:
                tomorrow_day_page = get_page_source(tomorrow_day_url)
                if tomorrow_day_page:
                    tomorrow_day = BeautifulSoup(tomorrow_day_page,
                                                 'html.parser')
                    weather_details = tomorrow_day.find('div',
                                             attrs={'id': 'detail-day-night'})
                    condition = weather_details.find('div', class_='cond')
                    if condition:
                        weather_info['cond'] = condition.text
                    temp = weather_details.find('span', class_='large-temp')
                    if temp:
                        weather_info['temp'] = temp.text
                    feal_temp = weather_details.find('span', 
                                                     class_='realfeel')
                    if feal_temp:
                        weather_info['feal_temp'] = feal_temp.text

    return weather_info


def get_weather_info_rp5(page_content, tomorrow=False):
    """ Getting the final result in tuple from site rp5.
    """

    city_page = BeautifulSoup(page_content, 'html.parser')
    weather_info = {}
    if not tomorrow:
        current_day_selection = city_page.find('div',
                                               class_='forprint-about')
        if current_day_selection:
            part_url = current_day_selection.findPrevious('a').attrs['href']
            base_url = 'http://rp5.ua' 
            part_url = urllib.parse.quote(part_url)
            current_day_url = base_url + part_url
            if current_day_url:
                current_day_page = get_page_source(current_day_url)
                if current_day_page:
                    current_day = BeautifulSoup(current_day_page, 
                                                'html.parser')
                    weather_details = \
                        current_day.find('div', attrs={'id': 'archiveString'})
                    weather_details_cond = \
                        weather_details.find('div', class_='ArchiveInfo')
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
                    feal_temp = weather_details_feal_temp.find('span',
                                                           class_='t_0')
                    if feal_temp:
                        weather_info['feal_temp'] = feal_temp.text
    else:
        tomorrow_day_selection = city_page.find('div',
                                               class_='forprint-about')
        if tomorrow_day_selection:
            part_url = tomorrow_day_selection.findPrevious('a').attrs['href']
            part_url = urllib.parse.quote(part_url)
            base_url = 'http://rp5.ua' 
            tomorrow_day_url = base_url + part_url
            if tomorrow_day_url:
                tomorrow_day_page = get_page_source(tomorrow_day_url)
                if tomorrow_day_page:
                    tomorrow_day = BeautifulSoup(tomorrow_day_page, 
                                                 'html.parser')
                    weather_details = \
                        tomorrow_day.find('div', attrs={'id': 
                                                'forecastShort-content'})
                    weather_details_tomorrow = weather_details.find(
                                                'span', class_='second-part')
                    conditions = \
                            weather_details_tomorrow.findPrevious('b').text
                    condition_all = str(conditions[conditions.find(
                                                             'Завтра:')+28:])
                    condition = str(condition_all[condition_all.find(
                                                                   'F,')+3:])
                    if condition:
                        weather_info['cond'] = condition
                    temp = weather_details_tomorrow.find('span', class_='t_0')
                    if temp:
                        weather_info['temp'] = temp.text
                        
    return weather_info


def get_weather_info_sinoptik(page_content, tomorrow=False):
    """ Getting the final result in tuple from sinoptik.ua site.
    """

    city_page = BeautifulSoup(page_content, 'html.parser')
    weather_info = {}
    weather_details = city_page.find('div', class_='tabsContent')
    if not tomorrow:
        weather_details = city_page.find('div', class_='tabsContent')
        condition_weather_details = weather_details.find('div', 
                                      class_='wDescription clearfix')
        condition = condition_weather_details.find('div', 
                                                class_='description')
        if condition:
            weather_info['cond'] = condition.text
        temp = weather_details.find('p', class_='today-temp')
        if temp:
            weather_info['temp'] = temp.text
            weather_details_feal_temp = weather_details.find('tr',
                                        class_='temperatureSens')
        feal_temp = weather_details_feal_temp.find('td', class_='p5 cur')
        if feal_temp:
            weather_info['feal_temp'] = feal_temp.text
    else:
        weather_details = city_page.find('div', attrs={'id': 'bd2'})
        condition = weather_details.find(
                    'div', class_='weatherIco d300')
        if condition:
            weather_info['cond'] = condition.text
        temp = weather_details.find('div', class_='max')
        if temp:
            weather_info['temp'] = temp.text
        feal_temp = weather_details.find('div', class_='min')
        if feal_temp:
            weather_info['feal_temp'] = feal_temp.text

    return weather_info


def produse_output(city_name, info):
    """ Displays the final result of the program
    """

    print(f'{city_name}')
    print('-'*20)
    for key, value in info.items():
        print(f' {key} : {html.unescape(value)}')


def get_accu_weather_info(tomorrow=False, write=False):
    """ Displays the weather information from AccuWeather site to current or
        tomorrow day, records this informations in a text file if you want.
    """

    city_name, city_url = get_configuration_accu()
    content = get_page_source(city_url)

    if not tomorrow:
        print("AccuWeather today: \n" + '-'*20)
    else:
        print("AccuWeather tomorrow: \n" + '-'*20)
    produse_output(city_name, get_weather_info_accu(content, 
                                                    tomorrow=tomorrow))
    if write==True:
        with open('weatherapp.txt', 'w') as f:
            f.write('AccuWeather tomorrow: ' + str(
                    get_weather_info_accu(content, tomorrow=tomorrow)))
    

def get_rp5_weather_info(tomorrow=False, write=False):
    """ Displays the weather information from RP5.ua site to current or
        tomorrow day, records this informations in a text file if you want.
    """

    city_name, city_url = get_configuration_rp5()
    content = get_page_source(city_url)

    if not tomorrow:
        print("RP5 today: \n" + '-'*20)
    else:
        print("RP5 tomorrow: \n" + '-'*20)
    produse_output(city_name, get_weather_info_rp5(content, 
                                                       tomorrow=tomorrow))

    if write==True:
        with open('weatherapp.txt', 'w') as f:
            f.write('RP5 tomorrow: ' + str(
                            get_weather_info_rp5(content, tomorrow=tomorrow)))


def get_sinoptik_weather_info(tomorrow=False, write=False):
    """ Displays the weather information from sinoptik site to current or
        tomorrow day, records this informations in a text file if you want.
    """

    city_name, city_url = get_configuration_sinoptik()
    content = get_page_source(city_url)

    if not tomorrow:
        print("SINOPTIK.UA today: \n" + '-'*20)
    else:
        print("SINOPTIK.UA tomorrow: \n" + '-'*20)
    produse_output(city_name, get_weather_info_sinoptik(content, 
                                                       tomorrow=tomorrow))
    if write==True:
        with open('weatherapp.txt', 'w') as f:
            f.write('SINOPTIK.UA: ' + str(
                                        get_weather_info_sinoptik(content, 
                                        tomorrow=tomorrow)))


def main(argv):
    """ Main entry point.
    """

    KNOWN_COMMANDS = {'accu': get_accu_weather_info, 'rp5': 
                       get_rp5_weather_info, 'sinoptik': 
                       get_sinoptik_weather_info}

    CONFIG_COMANDS = {'config_accu': configurate_accu, 'config_rp5': 
                       configurate_rp5, 'config_sinoptik': 
                       configurate_sinoptik}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    parser.add_argument('--tomorrow', help='weather for tomorrow day', 
                        action = 'store_true')
    parser.add_argument('--write_file', 
                        help='write the weather info to the text file', 
                        action = 'store_true')
    params = parser.parse_args(argv)

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            KNOWN_COMMANDS[command](tomorrow=params.tomorrow, 
                                    write=params.write_file) 
        elif command in CONFIG_COMANDS:
            CONFIG_COMANDS[command]()
        else:
            print("Unknown command provided!")
            sys.exit(1)



if __name__ == '__main__':
    main(sys.argv[1:])
