import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import csv

path = r"I:\bajaj hackrx\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(path)

# Login
def login():
    login_file = open('login.txt')
    line = login_file.readlines()

    email = line[0].strip()  # Remove leading/trailing whitespaces
    password = line[1].strip()

    driver.get("https://www.linkedin.com/login")
    time.sleep(1)

    eml = driver.find_element(by=By.ID, value="username")
    eml.send_keys(email)
    passwd = driver.find_element(by=By.ID, value="password")
    passwd.send_keys(password)
    loginbutton = driver.find_element(by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
    loginbutton.click()
    time.sleep(3)

# Return all profile URLs of M&A employees of a certain company
def getProfileURLs(companyName):
    driver.get(f"https://www.linkedin.com/company/{companyName}/people/?keywords=M%26A%2CMergers%2CAcquisitions")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    source = BeautifulSoup(driver.page_source, "html.parser")

    visibleEmployeesList = []
    visibleEmployees = source.find_all('a', class_='app-aware-link')
    for profile in visibleEmployees:
        if profile.get('href').split('/')[3] ==  'in':
            visibleEmployeesList.append(profile.get('href'))

    invisibleEmployeeList = []
    invisibleEmployees = source.find_all('div', class_='artdeco-entity-lockup artdeco-entity-lockup--stacked-center artdeco-entity-lockup--size-7 ember-view')
    for invisibleguy in invisibleEmployees:
        title = invisibleguy.findNext('div', class_='lt-line-clamp lt-line-clamp--multi-line ember-view').contents[0].strip('\n').strip('  ')
        invisibleEmployeeList.append(title)

        # A profile can either be visible or invisible
        profilepiclink = ""
        visibleProfilepiclink = invisibleguy.find('img', class_='lazy-image ember-view')
        invisibleProfilepicLink = invisibleguy.find('img', class_='lazy-image ghost-person ember-view')
        if visibleProfilepiclink is None:
            profilepiclink = invisibleProfilepicLink.get('src')
        else:
            profilepiclink = visibleProfilepiclink.get('src')

        if profilepiclink not in invisibleEmployees:
            invisibleEmployeeList.append(profilepiclink)
    
    return (visibleEmployeesList[5:], invisibleEmployeeList)

# Parses a type 2 job row
def parseType2Jobs(alltext):
    jobgroups = []
    company = alltext[16][:len(alltext[16]) // 2]
    totalDurationAtCompany = alltext[20][:len(alltext[20]) // 2]

    # Get rest of the jobs in the same nested list
    groups = []
    count = 0
    index = 0
    for a in alltext:
        if a == '' or a == ' ':
            count += 1
        else:
            groups.append((count, index))
            count = 0
        index += 1

    numJobsInJoblist = [g for g in groups if g[0] == 21 or g[0] == 22 or g[0] == 25 or g[0] == 26]
    for i in numJobsInJoblist:
        # Full time/part-time case
        if 'time' in alltext[i[1] + 5][:len(alltext[i[1] + 5]) // 2].lower().split('-'):
            jobgroups.append((alltext[i[1]][:len(alltext[i[1]]) // 2], alltext[i[1] + 8][:len(alltext[i[1] + 8]) // 2]))
        else:
            jobgroups.append((alltext[i[1]][:len(alltext[i[1]]) // 2], alltext[i[1] + 4][:len(alltext[i[1] + 4]) // 2]))
    
    return ('type2job', company, totalDurationAtCompany, jobgroups)

# Parses a type 1 job row
def parseType1Job(alltext):
    jobtitle = alltext[16][:len(alltext[16]) // 2]
    company = alltext[20][:len(alltext[20]) // 2]
    duration = alltext[23][:len(alltext[23]) // 2]
    return ('type1job', jobtitle, company, duration)

# Returns LinkedIn profile information
def returnProfileInfo(employeeLink, companyName):
    url = employeeLink
    driver.get(url)
    time.sleep(2)
    source = BeautifulSoup(driver.page_source, "html.parser")

    profile = []
    profile.append(companyName)
    info = source.find('div', class_='mt2 relative')
    name = info.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip()
    title = info.find('div', class_='text-body-medium break-words').get_text().lstrip().strip()
    profile.append(name)
    profile.append(title)
    time.sleep(1)
    experiences = source.find_all('li', class_='artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')

    for x in experiences[1:]:
        alltext = x.getText().split('\n')
        startIdentifier = 0
        for e in alltext:
            if e == '' or e == ' ':
                startIdentifier += 1
            else:
                break
        
        if startIdentifier == 16:
            # Education
            if 'university' in alltext[16].lower().split(' ') or 'college' in alltext[16].lower().split(' ') or 'ba' in alltext[16].lower().split(' ') or 'bs' in alltext[16].lower().split(' '):
                profile.append(('education', alltext[16][:len(alltext[16]) // 2], alltext[20][:len(alltext[20]) // 2]))
            # Certifications
            elif 'issued' in alltext[23].lower().split(' '):
                profile.append(('certification', alltext[16][:len(alltext[16]) // 2], alltext[20][:len(alltext[20]) // 2]))

        elif startIdentifier == 12:
            # Skills
            if (alltext[16] == '' or alltext[16] == ' ') and len(alltext) > 24:
                profile.append(('skill', alltext[12][:len(alltext[12]) // 2]))

    # Experiences
    url = driver.current_url + '/details/experience/'
    driver.get(url)
    time.sleep(2)
    source = BeautifulSoup(driver.page_source, "html.parser")
    time.sleep(1)
    exp = source.find_all('li')
    for e in exp[13:]:
        row = e.getText().split('\n')
        if row[:16] == ['', '', '', '', '', '', ' ', '', '', '', '', '', '', '', '', '']:
            if 'yrs' in row[20].split(' '):
                profile.append(parseType2Jobs(row))
            else:
                profile.append(parseType1Job(row))
    
    return profile

if __name__ == "__main__":
    companies = ['apple'] # Add other company names here if needed
    login()
    employees = {}
    for company in companies:
        searchable = getProfileURLs(company)
        for employee in searchable[0]:
            employees[employee] = returnProfileInfo(employee, company)

    # Save the data in CSV file
    with open('profile_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Company', 'Name', 'Title', 'Type', 'Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for employee, info in employees.items():
            company_name, name, title, *profile_info = info
            for item in profile_info:
                if isinstance(item, tuple):
                    writer.writerow({'Company': company_name, 'Name': name, 'Title': title, 'Type': item[0], 'Value': item[1]})
                elif isinstance(item, list):
                    for job in item:
                        writer.writerow({'Company': company_name, 'Name': name, 'Title': title, 'Type': job[0], 'Value': job[1]})

    time.sleep(10)
    driver.quit()

