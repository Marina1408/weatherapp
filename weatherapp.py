# -*- coding: utf-8 -*-
#!/usr/bin/python3

""" Weather add project.
"""

import html
from urllib.request import urlopen, Request

AKKU_URL = "https://www.accuweather.com/en/ua/rivne/325590/weather-forecast/325590?lang=en-us"

# getting page from server
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
accu_request = Request(AKKU_URL, headers = headers)
accu_page = urlopen(accu_request).read()
accu_page = str(accu_page)

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
accu_cond = u''
for char in accu_page[accu_cond_value_start:]:
	if char != '<':
		accu_cond += char
	else:
		break

print('AccuWeather: \n')
print(f'Temperature: {html.unescape(accu_temp)}\n')
print(f'Weather conditions: {html.unescape(accu_cond)}\n')






