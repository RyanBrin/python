# Project: Get GitHub Profile Views
# Author: Ryan Brinkman
# Date: 11/18/2024
# Repository: https://github.com/RyanBrin/python/tree/main/random-programs/get-github-profile-views/

import requests
from time import sleep

# URL to open
url = "https://camo.githubusercontent.com/6728cdfcb4d21b70af5602dddca651aaac3b5abb4de2ef66bb384435d10a0d26/68747470733a2f2f6b6f6d617265762e636f6d2f67687076632f3f757365726e616d653d7279616e6272696e266c6162656c3d50726f66696c65253230766965777326636f6c6f723d306537356236267374796c653d666c6174"

# Loop to open and close the URL repeatedly
while True:
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Optionally, check the status code to confirm it loaded correctly
    if response.status_code == 200:
        print("Page loaded successfully!")
    else:
        print(f"Failed to load page. Status code: {response.status_code}")
    
    # Wait for a short time before the next request (you can adjust the sleep time)
    sleep(0.1)  # Delay between requests