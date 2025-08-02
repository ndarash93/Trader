import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("INFLUX_TOKEN")
HOST = os.getenv("HOST")
BUCKET = os.getenv("BUCKET")
ORG = os.getenv("ORG")

class Flux:
  def __init__(self, influx_url, org, bucket, token):
    self.influx_url = influx_url  # e.g. "http://localhost:8086"
    self.bucket = bucket
    self.org = org
    self.token = token

  def push_to_influxdb(self, confirmed, unconfirmed, price, address):
    query = f'''
    from(bucket: "{BUCKET}")
    |> range
    '''
    url = f"{self.influx_url}/api/v2/write?bucket={self.bucket}&org={self.org}&precision=ns"
    headers = {
      "Authorization": f"Token {self.token}",
      "Content-Type": "text/plain"
    }

    r = requests.post(url, headers=headers, data=line)
    if r.status_code != 204:
      pass
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

  flux.push_to_influxdb(12345678, 1234, 100000, "bc1qyouraddress")
