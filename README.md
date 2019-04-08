                      **Project "weatherapp.core"**


What is it?
-----------

The purpose of this program is to display weather information from different sites or, if necessary, from one. We often see weather conditions from two-three sites for more reliable information. This program will allow to view weather information at the same time from three sites(AccuWeather, RP5 and Sinopik.ua) in a convenient format. Thanks to this the program saves time considerably in search of weather conditions.

Weatherapp.core:

* a program that collects weather information from the sites of AccuWeather, RP5.ua and sinoptik.ua;
* shows information of your choice in the form of a table, a list, a CSV or a text file;
* ability to display weather information today or tomorrow;
* ability to configure the place for which the program displays the weather information for each site, as well as the ability to erase the settings for each site;
* possibility to configure login, namely to set the level of logging, where to log (in the console or in a file), specify the name of the log file;
* program at startup deletes the outdated cache, but if desired, you can at any time completely delete the entire cache or take data only from the original site, rather than from the cache;
* the program has a simple user interface;
* the ability to add a new resource without changing the implementation of the main functional;
* the possibility of further development and development of programs.


Installation
------------

Download the repository to your machine and use the following command to locally install the package:

$ pip install .

Download repositories of the weather providers here:

weatherapp.accu       <https://github.com/Marina1408/weatherapp.accu>
weatherapp.rp5        <https://github.com/Marina1408/weatherapp.rp5>
weatherapp.sinoptik   <https://github.com/Marina1408/weatherapp.sinoptik>

Install each of these packages:

$ pip install .


Usage:
------

* get the weather data from all providers

  $ wfapp

* get weather data from a specific provider

  $ wfapp [provider id]

* get a list of all providers:

  $ wfapp providers

* get the weather data for tomorrow:

  $ wfapp --tomorrow
  $ wfapp [provider id] --tomorrow

* get the weather data into a text file:

  $ $ wfapp --write_file
  $ wfapp [provider id] --write_file

* get the weather data in a specific format(a table, a list or a CSV file, by default the list is set):

  $ wfapp --formatter=table
  $ wfapp --formatter=csv

* you can also change (if you want) formatter table parameters:

  ** set the right or centre alignment(by default to set the left alignment):

    $ wfapp --formatter=table align=r

    $ wfapp --formatter=table align=c

  ** specify the padding width(by default to set '1'):

    $ wfapp --formatter=table -padding_width=[the specified number]

  ** set the style of vertical separators(by default to set '2'):

    $ wfapp --formatter=table --vrules=[the specified number from 0 to 2]

  ** set the style of horizontal splitters(by default to set '0'):

    $ wfapp --formatter=table -hrules=[the specified number from 0 to 3]

* clear cache:

  $ wfapp clear_cache

* update cache:

  $ wfapp --refresh
  $ wfapp [provider id] --refresh

* select a location to get weather data from a specific provider:

  $ wfapp configurate [provider id]

* remove default locations in the configuration file

  $ wfapp configurate --reset_defaults

* configure login, namely to set the level of logging, where to log (in the console or in a file), specify the name of the log file

  $ wfapp configurate

* see a full trancback for errors:

  $ wfapp [command] --debug

* for setting the login level of the program(default WARNING) INFO:

  $ wfapp [command] -v  

* for setting the login level of the program(default WARNING) DEBUG:

  $ wfapp [command] -vv 


