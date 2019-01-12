#!/usr/bin/python3

""" Weather add project from accuweather and rp5
"""

import html
from urllib.request import urlopen, Request

AKKU_URL = "https://www.accuweather.com/uk/ua/rivne/325590/weather-forecast/325590"

# getting page from server
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
accu_request = Request(AKKU_URL, headers = headers)
accu_page = urlopen(accu_request).read()
accu_page = str(accu_page.decode())

ACCU_TEMP_TAG = '<span class="large-temp">'
accu_temp_tag_size = len(ACCU_TEMP_TAG)
accu_temp_tag_index = accu_page.find(ACCU_TEMP_TAG)
accu_temp_value_start = accu_temp_tag_index + accu_temp_tag_size
accu_temp = ''
for char in accu_page[accu_temp_value_start:]:
	if char != '<':
		accu_temp += char
	else:
		break

ACCU_COND_TAG = '<span class="cond">'
accu_cond_tag_size = len(ACCU_COND_TAG)
accu_cond_tag_index = accu_page.find(ACCU_COND_TAG)
accu_cond_value_start = accu_cond_tag_index + accu_cond_tag_size
accu_cond = ''
for char in accu_page[accu_cond_value_start:]:
	if char != '<':
		accu_cond += char
	else:
		break

print('AccuWeather: \n')
print(f'Temperature: {html.unescape(accu_temp)}\n')
print(f'Weather conditions: {html.unescape(accu_cond)}\n')

rp5_URL = "http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A0%D1%96%D0%B2%D0%BD%D0%BE%D0%BC%D1%83,_%D0%A0%D1%96%D0%B2%D0%BD%D0%B5%D0%BD%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C"

# getting page from server
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
rp5_request = Request(rp5_URL, headers = headers)
rp5_page = urlopen(rp5_request).read()
rp5_page = str(rp5_page.decode())

rp5_TEMP_TAG = '<span class="t_0" style="display: block;">'
rp5_temp_tag_size = len(rp5_TEMP_TAG)
rp5_temp_tag_index = rp5_page.find(rp5_TEMP_TAG)
rp5_temp_value_start = rp5_temp_tag_index + rp5_temp_tag_size
rp5_temp = ''
for char in rp5_page[rp5_temp_value_start:]:
	if char != '<':
		rp5_temp += char
	else:
		break

rp5_COND_TAG = '</span><span class="t_1" style="display: none;">°F</span>,</span> '
rp5_cond_tag_size = len(rp5_COND_TAG)
rp5_cond_tag_index = rp5_page.find(rp5_COND_TAG)
rp5_cond_value_start = rp5_cond_tag_index + rp5_cond_tag_size
rp5_cond = ''
for char in rp5_page[rp5_cond_value_start:]:
	if char != '<':
		rp5_cond += char
	else:
		break

print('rp5: \n')
print(f'Temperature: {html.unescape(rp5_temp)}\n')
print(f'Weather conditions: {html.unescape(rp5_cond)}\n')




