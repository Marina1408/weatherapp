#!/usr/bin/env python

""" Weather add project from accuweather, rp5 and sinoptik.ua
"""

import sys
import os
import html
import argparse
from pathlib import Path
from shutil import rmtree

from providers import AccuWeatherProvider
from providers import Rp5WeatherProvider
from providers import SinoptikWeatherProvider




def get_accu_weather_info(tomorrow=False, write=False, refresh=False):
    """ Displays the weather information from AccuWeather site to current or
        tomorrow day, records this informations in a text file if you want.
    """

    accu = AccuWeatherProvider()
    
    if not tomorrow:
        print("AccuWeather today: \n" + '-'*20)
    else:
        print("AccuWeather tomorrow: \n" + '-'*20)
    produse_output(accu.location, accu.run( tomorrow=tomorrow, 
                                            refresh=refresh))
    if write:
        with open('weatherapp.txt', 'w') as f:
            f.write('AccuWeather tomorrow: ' + str(
                            accu.run(tomorrow=tomorrow, refresh=refresh)))
    

def get_rp5_weather_info(tomorrow=False, write=False, refresh=False):
    """ Displays the weather information from RP5.ua site to current or
        tomorrow day, records this informations in a text file if you want.
    """

    rp5 = Rp5WeatherProvider()

    if not tomorrow:
        print("RP5 today: \n" + '-'*20)
    else:
        print("RP5 tomorrow: \n" + '-'*20)
    produse_output(rp5.location, rp5.run(tomorrow=tomorrow, refresh=refresh))

    if write:
        with open('weatherapp.txt', 'w') as f:
            f.write('RP5 tomorrow: ' + str(
                            rp5.run(tomorrow=tomorrow, refresh=refresh)))


def get_sinoptik_weather_info(tomorrow=False, write=False, refresh=False):
    """ Displays the weather information from sinoptik site to current or
        tomorrow day, records this informations in a text file if you want.
    """

    sinoptik = SinoptikWeatherProvider()

    if not tomorrow:
        print("SINOPTIK.UA today: \n" + '-'*20)
    else:
        print("SINOPTIK.UA tomorrow: \n" + '-'*20)
    produse_output(sinoptik.location, sinoptik.run( 
                                        tomorrow=tomorrow, refresh=refresh))
    if write:
        with open('weatherapp.txt', 'w') as f:
            f.write('SINOPTIK.UA: ' + str(sinoptik.run( 
                                        tomorrow=tomorrow, refresh=refresh)))


def clear_all_cache():
    """ Clear all cache files and the cache directory.
    """

    accu = AccuWeatherProvider()

    cache_dir = accu.get_cache_directory()
    rmtree(cache_dir)


def clear_not_valid_cache():
    """ Clear all not valid cache.
    """

    accu = AccuWeatherProvider()

    cache_dir = accu.get_cache_directory()
    if cache_dir.exists():
        for file in os.listdir(cache_dir):
            if not accu.is_valid(cache_dir/file):
                os.remove(cache_dir/file)
                           

def main(argv):
    """ Main entry point.
    """

    accu = AccuWeatherProvider()
    rp5 = Rp5WeatherProvider()
    sinoptik = SinoptikWeatherProvider()

    KNOWN_COMMANDS = {'accu': get_accu_weather_info, 'rp5': 
                       get_rp5_weather_info, 'sinoptik': 
                       get_sinoptik_weather_info}

    CONFIG_COMANDS = {'config_accu': accu.configurate_accu, 'config_rp5': 
                       rp5.configurate_rp5, 'config_sinoptik': 
                       sinoptik.configurate_sinoptik}

    CACHE_COMMANDS = {'clear-cache' : clear_all_cache}


    clear_not_valid_cache()
      
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    parser.add_argument('--tomorrow', help='Weather for tomorrow day', 
                        action = 'store_true')
    parser.add_argument('--write_file', 
                        help='Write the weather info to the text file', 
                        action = 'store_true')
    parser.add_argument('--refresh', help='Update caches', 
                        action = 'store_true')
    parser.add_argument('clear-cache', 
                        help='Clear all cache with cache directory', 
                        nargs='?')
    parser.add_argument('--reset_defaults', 
                        help='Clear configurate locations', 
                        action = 'store_true')
    params = parser.parse_args(argv)

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            KNOWN_COMMANDS[command](tomorrow=params.tomorrow, 
                                    write=params.write_file,
                                    refresh=params.refresh) 
        elif command in CONFIG_COMANDS:
            CONFIG_COMANDS[command](refresh=params.refresh, 
                                    r_defaults=params.reset_defaults)
        elif command in CACHE_COMMANDS:
            CACHE_COMMANDS[command]()
        else:
            print("Unknown command provided!")
            sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
