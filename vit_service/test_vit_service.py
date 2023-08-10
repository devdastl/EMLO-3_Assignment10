import requests
import time
import logging
import os

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

url = "http://localhost:8080/vit_inference"

response_time = []

for i in range(1, 101):

  payload={}
  test_image_path = os.path.join('vit_service', 'test_image', 'test.jpg')
  files=[
    ('file',('test.jpg',open(test_image_path,'rb'),'image/jpeg'))
  ]
  headers = {
    'accept': 'application/json'
  }

  start_time = time.time()
  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  end_time = time.time()
  time_taken = round(end_time - start_time, 3)

  response_time.append(time_taken)

  if response.status_code == 200:
      log.info(f"API call for VIT service was successful!, time taken to process request {i}: {time_taken} seconds")
  else:
      log.info(f"API call for request {i} failed")
  pass

log.info(f"Average time of processing VIT service 100 API calls: {sum(response_time)/(len(response_time))}")