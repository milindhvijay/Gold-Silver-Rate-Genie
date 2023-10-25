import os
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import subprocess
from dotenv import load_dotenv

load_dotenv()

rates_file_path = os.getenv("RATES_FILE_PATH")
message_send_file = os.getenv("MESSAGE_SEND_FILE")
rates_url = os.getenv("RATES_URL")

url = rates_url

response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Extract gold and silver rates using regular expressions
rates = re.findall(r'(\d+)\s*\/GM', soup.text)

# Get today's date in the format "dd/mm/yyyy"
current_date = datetime.now().strftime("%d/%m/%Y")

last_updated_date = re.search(r'Last updated : (\d{2}/\d{2}/\d{4})', soup.find(string=re.compile('Last updated'))).group(1)

if os.path.exists(rates_file_path):
    with open(rates_file_path) as f:
        lines = f.readlines()
        existing_date = lines[0].split(':')[1].strip()

# Check if existing date matches scraped date
if not os.path.exists(rates_file_path) or last_updated_date != existing_date:
    # Rates outdated, update and send notifications
    with open(rates_file_path, 'w') as f:
        f.write(f'Date: {last_updated_date}\n') 
        f.write(f'Gold Rate: ₹{rates[1]}/-\n')
        f.write(f'Silver Rate: ₹{rates[3]}/-\n')

    subprocess.run(["python3", message_send_file])

else:
    print('Unchanged')

