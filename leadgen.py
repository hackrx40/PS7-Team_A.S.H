import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_to_mouthshut(username, password):
    # Start the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Open the login page
        driver.get("https://www.mouthshut.com/login")

        # Wait for the email input field to be visible
        email_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "msLoginEmail"))
        )

        # Enter username and password and submit the form
        email_input.send_keys(username)
        driver.find_element(By.ID, "msLoginPassword").send_keys(password)
        driver.find_element(By.ID, "login-form-btn").click()

        # Wait for the login to complete (you may need to adjust the wait time based on your internet speed)
        time.sleep(5)

        return driver
    except Exception as e:
        print("Error during login:", e)
        driver.quit()
        return None

def extract_data(driver, url):
    try:
        # Open the URL
        driver.get(url)

        # Find the parent element containing all reviews
        reviews_parent_element = driver.find_element(By.XPATH, "//div[@id='dvreview-listing']")

        # Find all comment elements
        comment_elements = reviews_parent_element.find_elements(By.XPATH, ".//div[contains(@class, 'reviewdata')]//div[contains(@class, 'more reviewdata-expander')]/preceding-sibling::text()")

        # Find all user profiles
        user_profiles = reviews_parent_element.find_elements(By.XPATH, ".//div[contains(@class, 'reviewer-profile')]/a")

        # Find all links to user profile pages
        user_profile_links = [profile.get_attribute("href") for profile in user_profiles]

        # Store the data in a list of dictionaries
        data_list = []
        for i, comment_element in enumerate(comment_elements):
            comment = comment_element.strip()
            user_profile = user_profiles[i].text.strip()
            user_profile_link = user_profile_links[i]
            data_list.append({"Comment": comment, "User Profile": user_profile, "User Profile Link": user_profile_link})

        return data_list

    except Exception as e:
        print("Error during data extraction:", e)
        return []

def save_to_csv(data_list, file_name):
    # Save the data to a CSV file
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Comment", "User Profile", "User Profile Link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_list:
            writer.writerow(data)

if __name__ == "__main__":
    # Input your MouthShut username and password
    username = input("Enter your MouthShut email: ")
    password = input("Enter your MouthShut password: ")

    # URL of the page you want to scrape
    url = "https://www.mouthshut.com/product-reviews/Patanjali-Dant-Kanti-Toothpaste-reviews-925011850"

    # File name to save the CSV data
    file_name = "mouthshut_reviews.csv"

    # Login to MouthShut
    driver = login_to_mouthshut(username, password)

    if driver:
        # Extract data from the desired page
        data_list = extract_data(driver, url)

        # Save the data to CSV
        save_to_csv(data_list, file_name)

        # Close the browser window
        driver.quit()
