# packages

from bs4 import BeautifulSoup
import requests

# scan for date

print("Enter year (4-digit number): ")
year = input()
print("Enter month (2-digit number): ")
month = input()

# get page to scrape

url = "https://game.capcom.com/cfn/sfv/stats/usagerate/%s%s" % (year, month)

# define scraping methods

response = requests.get(url, timeout = 5)
soup = BeautifulSoup(response.content, "html.parser")

# create lists for fighters and usage rates

fighter = []
rate = []

# define date

date = soup.find('p', attrs={"class": "selectData"}).text

# place characters and rates into lists

for character in soup.findAll('p', attrs={"class":"name"}):
    fighter.append(character.text)

for use in soup.findAll('p', attrs={"class" : "percent"}):
    rate.append(use.text)

# combine characters and usage lists

charUsage = list(map(lambda x, y:(x,y), fighter, rate))

print("Character usage for " + date)
print(charUsage)
