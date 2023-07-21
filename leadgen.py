import requests
import csv
from datetime import datetime

def fetch_random_users(num_users=1):
    base_url = 'https://randomuser.me/api/'
    params = {
        'results': num_users,
        'nat': 'us',  # You can change the nationality code to get users from different countries.
    }

    response = requests.get(base_url, params=params)

    if response.ok:
        data = response.json()
        return data['results']
    else:
        response.raise_for_status()

def calculate_age(birth_date):
    birth_date = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def generate_dummy_leads(num_leads):
    users = fetch_random_users(num_leads)

    leads = []
    for user in users:
        lead = {
            'Name': f"{user['name']['first']} {user['name']['last']}",
            'Email': user['email'],
            'Phone': user['phone'],
            'City': user['location']['city'],
            'State': user['location']['state'],
            'Country': user['location']['country'],
            'DateOfBirth': user['dob']['date'],
            'Age': calculate_age(user['dob']['date']),
        }
        leads.append(lead)

    return leads

def save_leads_to_csv(leads, file_name):
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Email', 'Phone', 'City', 'State', 'Country', 'DateOfBirth', 'Age']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for lead in leads:
            writer.writerow(lead)

if __name__ == '__main__':
    num_leads_to_generate = 100  # Update this to generate 50 dummy leads
    leads = generate_dummy_leads(num_leads_to_generate)

    file_name = 'leaads.csv'
    save_leads_to_csv(leads, file_name)

    print(f"{num_leads_to_generate} dummy leads generated and saved to {file_name}.")


