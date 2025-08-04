import os
import time
import requests
import pandas
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("INFLUX_TOKEN")
HOST = os.getenv("HOST")
BUCKET = os.getenv("BUCKET")
ORG = os.getenv("ORG")

class Flux:
  def __init__(self, influx_url, org, bucket, token):
    self.influx_url = influx_url
    self.bucket = bucket
    self.org = org
    self.token = token

  def pull(self):
    query = f'''
    from(bucket: "{BUCKET}")
    |> range(start: 0)
    |> filter(fn: (r) => r["_measurement"] == "btc_balance")
    |> filter(fn: (r) => r["_field"] == "price")
    '''
    print('query', query)
    #url = f"{self.influx_url}/api/v2/query?bucket={self.bucket}&org={self.org}&precision=ns"
    url = f"{self.influx_url}/api/v2/query?org={self.org}"
    headers = {
      "Authorization": f"Token {self.token}"
      ,"Content-Type": "application/vnd.flux"
      #i,"Accept": "application/json"
    }

    r = requests.post(url, headers=headers, data=query)
    if r.status_code == 200:
      with open("btc_price.csv", "w", newline="") as f:
        f.write(r.text)
    else:
      pass

if __name__ == "__main__":
  # Usage example
  flux = Flux(
    influx_url=f"http://{HOST}:8086",
    org=ORG,
    bucket=BUCKET,
    token=TOKEN
  )

  #flux.pull()

  start = {"USD": 500, "BTC": 0.005}

  csv = pandas.read_csv('btc_price.csv')
  count = 0
  prev_price = csv['_value'][0]
  #print(csv['_value'][0])
  #"""
  data = []
  for index, row in csv.iterrows():
    dt = datetime.fromisoformat(row["_time"].rstrip('Z')[:26])
    val = row["_value"]
    data.append(dict(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute, price=val))
    if dt.hour == 0 and dt.minute == 0:
      change = (val - prev_price)/abs(prev_price)
      prev_price = val
      #print(change)
      #if change > 0:
      start["BTC"] = start["BTC"] * (1-(change))
      start["USD"] = start["USD"] + (change*start["BTC"]*val)
      print("Change:", change, "BTC:", start["BTC"], "USD:", start["USD"], "Total:", (start["USD"]/val) + start["BTC"])
      #else:
        #start["BTC"] = start["BTC"] * (1+change)

  
  #print(data)
  #"""

  #dt = datetime.fromisoformat("2025-05-22T22:50:00.502010")
  #print(dt.year)