from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

chrome_driver_path = '_____'  # replace with path (my data redacted)
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

output_file = 'public_domains.json'

all_domains = []

for page in range(1, 233):
    url = f'https://freedns.afraid.org/domain/registry/?page={page}'
    print(f"Scraping page {page}...")
    driver.get(url)
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    table_rows = soup.find_all('tr')[1:]
    for row in table_rows:
        cols = row.find_all('td')
        if len(cols) >= 3:
            domain = cols[0].text.strip()
            status = cols[1].text.strip().lower()
            if status == 'public':
                all_domains.append(domain)

# Save results as JSON instead of txt
with open(output_file, 'w') as f:
    json.dump(all_domains, f, indent=2)

print(f"\nScraped {len(all_domains)} public domains.")
print(f"Saved to {output_file}")

driver.quit()
