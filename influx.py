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
  csv = pandas.read_csv('btc_price.csv')
  count = 0

  data = []
  for index, row in csv.iterrows():
    time = datetime.fromisoformat(row["_time"].rstrip('Z')[:26])
    val = row["_value"]
    data.append(dict(time=time, price=val))
  print(data)
