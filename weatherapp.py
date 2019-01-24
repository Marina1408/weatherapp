#!/usr/bin/python3

""" Weather add project from accuweather, rp5 and sinoptik.ua
"""

import html
from urllib.request import urlopen, Request

ACCU_URL = ('https://www.accuweather.com/uk/ua/rivne/325590/'
            'weather-forecast/325590')
ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')
ACCU_CONTAINER_TAG = ('<div class="temp">')

RP5_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%'
           'A0%D1%96%D0%B2%D0%BD%D0%BE%D0%BC%D1%83,_%D0%A0%D1%96%D0%B2%D0%'
           'BD%D0%B5%D0%BD%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B'
           '0%D1%81%D1%82%D1%8C')
RP5_TAGS = ('<span class="t_0" style="display: block;">', '°F</span>')
RP5_CONTAINER_TAG = ('<div class="ArchiveTemp">', '<div class="ArchiveInfo">')


SINOPTIK_URL = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%'
                'D0%B0-%D1%80%D1%96%D0%B2%D0%BD%D0%B5')
SINOPTIK_TAGS = ('<p class="today-temp">', '<div class="description">'
                 ' <!--noindex--> ')
SINOPTIK_CONTAINER_TAG = (' ')


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


def get_tag_content(page_content, tag, container_tag):
    """Getting text from the page with tag.
    """
    def get_container_tag_content(page_content, tag, container_tag):
        """Getting text from the page with additional tags.
        """

        i = 0
        while i < len(container_tag):
            container = container_tag[i]
            if page_content.count(container) > 1:
                i += 1
            else:
                break

        tag_index = page_content.find(tag, page_content.find(container))
        return tag_index

    if page_content.count(tag) > 1:
        tag_index = get_container_tag_content(page_content, tag, container_tag)
    else:
        tag_index = page_content.find(tag)

    tag_size = len(tag)
    value_start = tag_index + tag_size
    content = ''
    for c in page_content[value_start:]:
        if c != '<':
            content += c
        else:
            break
    return content


def get_weather_info(page_content, tags, container_tag):
    """Getting the final result in tuple.
    """

    return tuple([get_tag_content(page_content, tag, container_tag)
                  for tag in tags])


def produse_output(provider_name, temp, condition):
    """Displays the final result of the program
    """

    print(f'\n{provider_name}:\n')
    print(f'Temperature: {html.unescape(temp)}\n')
    print(f'Weather conditions: {condition}\n')


def main():
    """Main entry point.
    """

    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS, ACCU_CONTAINER_TAG),
                     "RP5": (RP5_URL, RP5_TAGS, RP5_CONTAINER_TAG),
                     "SINOPTIK.UA": (SINOPTIK_URL, SINOPTIK_TAGS,
                                     SINOPTIK_CONTAINER_TAG)}
    for name in weather_sites:
        url, tags, container_tag = weather_sites[name]
        content = get_page_source(url)
        temp, condition = get_weather_info(content, tags, container_tag)
        produse_output(name, temp, condition)


if __name__ == '__main__':
    main()
