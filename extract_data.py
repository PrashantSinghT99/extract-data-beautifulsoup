# Import the requests module, which allows you to send HTTP requests
import requests
from bs4 import BeautifulSoup
import json
import time

#url to fetch all the records for directory https://www.ciffa.com/member-directory/
#handled email address loading and infinity scrolling by clicking on load more button
url = "https://www.ciffa.com/wp-admin/admin-ajax.php"
offset = 0
data = []

while True:
    params = {
        "action": "members_dir",
        "nonce": "30bbefb204",
        "province": "",
        "expertise": "",
        "membership_type": "",
        "searchfilter": "",
        "offset": offset
    }

    response = requests.post(url, data=params)
    response_data = response.json()

    if not response_data.get('success', False):
        break

    html_data = response_data.get('data', {}).get('html', '')

    if not html_data:
        break

    soup = BeautifulSoup(html_data, "html.parser")
    cards = soup.find_all("div", class_="membership-dir-card")

    for card in cards:
        card_company = card.find("div", "company").text.split(":")[1].strip()
        card_location = card.find("div", "location").text.split(":")[1].strip()
        card_emails = [email.a.text for email in card.find_all("span", class_="email")]
        data.append({"Name": card_company, "Location": card_location, "Emails": card_emails})

    offset += 25
    time.sleep(1)

# Write the data to a JSON file
with open("extracted_data.json", "w") as file:
    json.dump(data, file, indent=4)

print("Data written to extracted_data.json")
