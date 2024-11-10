import requests
import json
import datetime as dt
import time
import sys

# get json data from FRA Airport today
dt = dt.date.today()
# date in string
date = str(dt)
# time in string
time = time.strftime("%H:%M:%S")
# server url
URLstart = "https://www.frankfurt-airport.com/de/_jcr_content.flights.json/filter?perpage=9&lang=de-DE&page=1&flighttype=departures&time="
# combine strings to get final URL to get information
URL = URLstart + date + time +"Z"

# retrieve json package with flight data
page = requests.get(URL)
# safe json data in cont var
cont = page.json()

# get data from content
data = cont.get("data")
# define outputlist for Vestaboard
outputlist = ""
# set flight count to zero
count = 0

for k in data:
  #print(k.get("fnr"))
  tempstr = ""
  #check if it is a train
  if k.get("gate")[:1] == "T":
    tempstr= tempstr
  else:
    #set flight status to according colorcode
    if k.get("status") == "":
      tempstr += "{70}" #black
    elif k.get("status") == "Boarding":
      tempstr += "{66}" #orange
    elif k.get("status") == "Gate offen":
      tempstr += "{64}" #green
    elif k.get("status") == "geschlossen":
      tempstr += "{63}" #red
    else:
      tempstr += " " #leave blank if no status applies
    
    #set flight number and spaces
    if len(k.get("fnr")) == 8:
      tempstr += k.get("fnr")[:3]+ k.get("fnr")[4:]
    elif len(k.get("fnr")) == 7:
      tempstr += k.get("fnr")
    elif len(k.get("fnr")) == 6:
      tempstr += k.get("fnr")[:2] + "  " + k.get("fnr")[3:]
    elif len(k.get("fnr")) == 5:
      tempstr += k.get("fnr")[:2] + "   " + k.get("fnr")[3:]  
    else:
      tempstr += "       "
    
    #set destination abbreviation
    if k.get("iata") is not None:
      tempstr += " " + k.get("iata") + " "
    else:
      tempstr += "     "
  
    #set gate and add spaces between characters
    print(k.get("gate"))
    if k.get("gate") is None:
      tempstr += "    "
    elif len(k.get("gate")) == 3:
      tempstr += k.get("gate") + " "
    else:
      tempstr += k.get("gate")[:1] + " " + k.get("gate")[1:] + " "

    #set scheduled time of arrival
    if k.get("sched") is not None:
      tempstr += str(k.get("sched"))[11:16]
    else:
      tempstr += "     "
  
    #combine all infos for 6 flights
    if count<6:
      outputlist+=tempstr
      count+= 1

# format the string to vestboard output
formatDisplay = requests.post('https://vbml.vestaboard.com/format', data='{"message": "'+outputlist+'"}', headers={'Content-Type': 'application/json'})

# post generated format to vestaboard
postDisplay = requests.post('https://rw.vestaboard.com/', data=formatDisplay.text, headers={'X-Vestaboard-Read-Write-Key': 'ADD YOUR KEY', 'Content-Type': 'application/json'})

#close the program
sys.exit()