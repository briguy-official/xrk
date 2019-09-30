# Kart Racing Data Analysis
# Brian Acosta 
# January 7th 
#
#
# Distributed under creative commons beerware license:
# Free, but if you use it and we ever meet you buy me a beer.

from xrk import *
import os 
import csv
import glob

# input day for which testing data is desired
year = int(input('Enter Year: '))
if year < 100:
    year += 2000
year_string = str(year)

month = int(input('Enter Month as a Number: '))
if month < 10:
    month_string = ('0%d' %month)
else:
    month_string = str(month)

day = int(input('Enter Day: '))
if day < 10:
    day_string = ('0%d' %day)
else:
    day_string = str(day)

folder_name = ('%s-%s-%s' %(year_string, month_string, day_string))
file_names = glob.glob('xrk_files/*/*.xrk')

runs = []

print('Files found:\n')

for fil in file_names:
    print('%s' %fil)