import requests
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

url = "http://localhost:8080/gpt_inference"

payload = json.dumps({
  "text": "the cross"
})
headers = {
  'accept': 'application/json',
  'Content-Type': 'application/json'
}

response_time = []

for i in range(1, 101):
    start_time = time.time()
    response = requests.request("POST", url, headers=headers, data=payload)
    end_time = time.time()
    time_taken = round(end_time - start_time, 3)

    response_time.append(time_taken)

    if response.status_code == 200:
        log.info(f"API call for GPT service was successful!, time taken to process request {i}: {time_taken} seconds")
    else:
        log.info(f"API call for request {i} failed")
    pass

log.info(f"Average time of processing 100 API calls of GPT service: {sum(response_time)/(len(response_time))}")