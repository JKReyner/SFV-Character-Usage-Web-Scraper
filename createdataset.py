# packages

from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

# initialize dates

today = datetime.today()
curYr = today.year
curMo = today.month

year = 2016
month = 10

# create sets to collect dates, fighters, usage

urlSet = []
dateSet = []
fighter = []
rate = []

# create a loop to get every viable url

while year < curYr or month < curMo:
    month2d = format(month, '02d')
    url = "https://game.capcom.com/cfn/sfv/stats/usagerate/%s%s" % (year, month2d)
    urlSet.append(url)
    month = (month % 12) + 1
    if month == 1:
        year += 1

# get usages for each month's reports

for url in urlSet:

    # define method to scrape each url

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # scrape the urls and add data to the sets

    for character in soup.findAll('p', attrs={"class":"name"}):
        fighter.append(character.text)

    for use in soup.findAll('p', attrs={"class" : "percent"}):
        rate.append(float(use.text.strip('%')))

# create an automatic set of dates to map onto the data set

# create a function that will check the values of the usage rates

i = 0
pos = 1

# reset dates

year = 2016
month = 10

while i <= len(rate):
    d = datetime(year=year, month=month, day=1)
    dateSet.append(d.strftime('%m-%Y'))

    # this segment will check if the entire set of fighters in the roster has been covered for a given month and will
    # advance to the next month once that has occured
    if rate[pos] > rate[pos - 1]:
        month = (month % 12) + 1
        if month == 1:
            year += 1
    pos += 1
    if pos > (len(rate) - 1):
        pos = (len(rate) - 1)
    i += 1

# create a single list for the usage rates

charUsage = list(map(lambda x, y, z:(x, y, z), fighter, rate, dateSet))

# export charUsage to csv, since character numbers change multiple times, a date column is better added manually

df = pd.DataFrame(charUsage, columns = ["Character", "Usage Rate", "Date"])

df.to_csv("%s - %s.csv" % (year, month))
