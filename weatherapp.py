#!/usr/bin/python3

""" Weather add project from accuweather, rp5 and sinoptik.ua
"""

import sys
import html
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


ACCU_URL = ('https://www.accuweather.com/uk/ua/rivne/325590/'
            'weather-forecast/325590')

RP5_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%'
           'A0%D1%96%D0%B2%D0%BD%D0%BE%D0%BC%D1%83,_%D0%A0%D1%96%D0%B2%D0%'
           'BD%D0%B5%D0%BD%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B'
           '0%D1%81%D1%82%D1%8C')

SINOPTIK_URL = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%'
                'D0%B0-%D1%80%D1%96%D0%B2%D0%BD%D0%B5')


def get_request_headers():
    """Getting headers of the request.
    """

    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}


def get_page_source(url):
    """Getting page from server.
    """

    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')


def get_weather_info_accu(page_content, day):
    """Getting the final result in tuple from site accuweather.
    """

    city_page = BeautifulSoup(page_content, 'html.parser')
    weather_info = {}
    if day == 'current':
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
    if day == 'tomorrow':
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
                    feal_temp = weather_details.find('span', class_='realfeel')
                    if feal_temp:
                        weather_info['feal_temp'] = feal_temp.text

    return weather_info


def get_weather_info_rp5(page_content):
    """Getting the final result in tuple from site rp5.
    """

    city_page = BeautifulSoup(page_content, 'html.parser')
    current_day_selection = city_page.find('div',
                                           class_='forprint-about')

    weather_info = {}
    if current_day_selection:
        current_day_url = current_day_selection.findPrevious('a').attrs['href']
        current_day_url = RP5_URL
        # current_day_url = 'http://rp5.ua' + '/Weather_in_Rivne'

        # print(current_day_url)
        # current_day_url = bytes(current_day_url, 'utf-8')
        # print(current_day_url)
        # current_day_url = current_day_url.decode(utf-8)
        # print(current_day_url)
        # current_day_url1 = 'http://rp5.ua' + current_day_url
        if current_day_url:
            current_day_page = get_page_source(current_day_url)
            if current_day_page:
                current_day = BeautifulSoup(current_day_page, 'html.parser')
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
    return weather_info


def get_weather_info_sinoptik(page_content, day):
    """Getting the final result in tuple from sinoptik.ua site.
    """

    city_page = BeautifulSoup(page_content, 'html.parser')
    # current_day_selection = city_page.find('div', attrs={'id' :
    # 'wrapper'})
    weather_info = {}
    current_day_selection = city_page
    if day == 'current':
        current_day_url = SINOPTIK_URL
        if current_day_url:
            current_day_page = get_page_source(current_day_url)
            if current_day_page:
                current_day = BeautifulSoup(current_day_page, 'html.parser')
                weather_details = current_day.find('div',
                                                   class_='tabsContentInner')
                condition = weather_details.find('div', class_='description')
                if condition:
                    weather_info['cond'] = condition.text
                temp = weather_details.find('p', class_='today-temp')
                if temp:
                    weather_info['temp'] = temp.text
                weather_details_feal_temp = weather_details.find('tr',
                                                    class_='temperatureSens')
                feal_temp = weather_details_feal_temp.find('td',
                                                           class_='p5 cur')
                if feal_temp:
                    weather_info['feal_temp'] = feal_temp.text
    if day == 'tomorrow':
        # tomorrow_day_selection =  city_page.find('div', attrs={'id' : 'bd2'})
        # if tomorrow_day_selection:
            # tomorrow_day_url = tomorrow_day_selection.find('a').attrs['href']
            # tomorrow_day_url = 'http:' + tomorrow_day_url
            # print(tomorrow_day_url)
        tomorrow_day_url = SINOPTIK_URL
        if tomorrow_day_url:
            tomorrow_day_page = get_page_source(tomorrow_day_url)
            if tomorrow_day_page:
                tomorrow_day = BeautifulSoup(tomorrow_day_page, 'html.parser')
                weather_details = tomorrow_day.find('div', attrs={'id': 'bd2'})
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


def produse_output(info):
    """Displays the final result of the program
    """

    for key, value in info.items():
        print(f' {key} : {html.unescape(value)}')


def main(argv):
    """Main entry point.
    """

    KNOWN_COMMANDS = {'accu': 'AccuWeather', 'rp5': 'RP5',
                      'sinoptik': 'SINOPTIK.UA'}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    parser.add_argument('tomorrow', help='Service name', nargs='?')
    parser.add_argument('write_file', help='Service name', nargs='?')
    params = parser.parse_args(argv)

    weather_sites = {"AccuWeather": (ACCU_URL),
                     "RP5": (RP5_URL),
                     "SINOPTIK.UA": (SINOPTIK_URL)}

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            weather_sites = {KNOWN_COMMANDS[command]:
                             weather_sites[KNOWN_COMMANDS[command]]}
        else:
            print("Unknown command provided!")
            sys.exit(1)

    for name in weather_sites:
        url = weather_sites[name]
        content = get_page_source(url)
        if command == 'accu':
            if params.tomorrow == 'tomorrow':
                print("AccuWeather tomorrow: \n")
                produse_output(get_weather_info_accu(content, day='tomorrow'))
                if params.write_file:
                    f = open('weatherapp.txt', 'w')
                    f.write(str(get_weather_info_accu(content, 
                    	        day='tomorrow')))
                    f.close()
            else:
                print("AccuWeather: \n")
                produse_output(get_weather_info_accu(content, day='current'))
                if params.write_file:
                    f = open('weatherapp.txt', 'w')
                    f.write(str(get_weather_info_accu(content, day='current')))
                    f.close()
        if command == 'rp5':
            print("RP5: \n")
            produse_output(get_weather_info_rp5(content))
            if params.write_file:
                f = open('weatherapp.txt', 'w')
                f.write(str(get_weather_info_rp5(content)))
                f.close()
        if command == 'sinoptik':
            if params.tomorrow == 'tomorrow':
                print("SINOPTIK.UA tomorrow: \n")
                produse_output(get_weather_info_sinoptik(
                    content, day='tomorrow'))
                if params.write_file:
                    f = open('weatherapp.txt', 'w')
                    f.write(str(get_weather_info_sinoptik(
                        content, day='tomorrow')))
                    f.close()
            else:
                print("SINOPTIK.UA: \n")
                produse_output(get_weather_info_sinoptik(
                    content, day='current'))
                if params.write_file:
                    f = open('weatherapp.txt', 'w')
                    f.write(str(get_weather_info_sinoptik(content,
                                day='current')))
                    f.close()


if __name__ == '__main__':
    main(sys.argv[1:])
