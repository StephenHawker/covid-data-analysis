covid data analysis -app.py - Ingest of covid data for UK
====================================

## Description

Extracts firestation location details from a specified URL, stores this data as csv file format.
The program then calculates the 3 closest firestations from a list of specified addresses 

## Written By Steve Hawker 01/01/2022

## Requirements

 - Python 3.7 or later.
 - The following Python libraries
   - configparser
   - urllib 
   - import urllib.parse
   - import urllib.parse as urlparse
   - import sys
   - import math
   - import logging
   - import logging.config
   - import io
   - import ssl
   - pandas
   - BeautifulSoup
   - requests
   - simplejson
   

## Run	

Configure covid_data.ini with the appropriate parameters
run app.py  (no parameters required) to scrape the website and download covid data

