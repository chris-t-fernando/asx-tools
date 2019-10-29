import json
import urllib2
from pushover import init, Client
#from datetime import date, datetime
import datetime
from dateutil.relativedelta import relativedelta, FR


init("aJcfJv8iqShDjjwXdg5A5eCRbwqvsH")

targetprice = {
    "avh": 0.56
}

# grab latest alphavantage json extract
avh = json.load(urllib2.urlopen("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey=%3CyourAPIKEY%3E&datatype=json&symbol=AVH.AX&outputsize=compact"))

# walk back through the avh dict day by day to find the most recent result
i = 0
walkLimit = 7 # how many days to walk back, including 0
today = datetime.date.today()

# for testing only
# today = datetime.date.today() + relativedelta(weekday=FR(2))

while i < walkLimit:
    i+=1
    pastDays = datetime.timedelta(days=i)
    currentDay = today - pastDays
    searchKey = str(currentDay.strftime('%Y-%m-%d'))
    
    if searchKey in avh["Time Series (Daily)"]:
        break
    
    if i == walkLimit:
        print "Could not find ASX data in the last " + str(walkLimit) + " calendar days - failing."
        Client("gCcFJwgAw48scLCTiR9Q2om92jGqUP").send_message("Could not find ASX data in the last " + str(walkLimit) + " calendar days - failing.", title="ASX price checker")
        exit()


# if date.today().weekday() == 0:
   # searchDate = datetime.now() + relativedelta(weekday=FR(-1))
   # print "Setting search date to: " + str(datetime.now() + relativedelta(weekday=FR(-1)))
# else:
   # searchDate = datetime.now()

#convert searchDate to yyyy-mm-dd
# searchKey = str(searchDate.strftime('%Y-%m-%d'))

if float(avh["Time Series (Daily)"][searchKey]["3. low"]) < targetprice["avh"]:
    print "AVH daily low of " + str(avh["Time Series (Daily)"][searchKey]["3. low"]) + " is lower than target price of " + str(targetprice["avh"])
    Client("gCcFJwgAw48scLCTiR9Q2om92jGqUP").send_message("AVH daily low of " + str(avh["Time Series (Daily)"][searchKey]["3. low"]) + " is lower than target price of " + str(targetprice["avh"]), title="ASX price checker")

elif today.weekday() == 0:
    Client("gCcFJwgAw48scLCTiR9Q2om92jGqUP").send_message("ASX heartbeat", title="ASX price checker")
    

