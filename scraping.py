import requests 
from bs4 import BeautifulSoup
def crawl_linkedin_profiles(target_keywords, max_profiles=100):
    base_url = "https://www.linkedin.com/search/results/people/?keywords="
    crawled_profiles=[] 
    for keyword in target_keywords:
        page_num=1
        while len(crawled_profiles)<max_profiles:
            url = f"{base_url}{keyword}&page={page_num}"
            response= requests.get(url)
            soup= BeautifulSoup(response.content, 'html.parser')
            profile_cards = soup.find_all("li",{"class":"reusable-search__result-container"})

            if not profile_cards:
                break

            for card in profile_cards:
                name=card.find("span",{"actor-name"}).text.strip()
                headline=card.find("div",{"class":"actor-description"}).text.strip()
                location=card.find("span",{"class":"actor-meta"}).text.strip()

                profile_data={
                    'name':name,
                    'headline':headline,
                    'location':location
                }

                crawled_profiles.append(profile_data)

                if len(crawled_profiles)>= max_profiles:
                    break
            page_nim+=1

    return crawled_profiles


target_keywords = ["data science", "marketing", "software engineering"]
linkedin_profiles=crawl_linkedin_profiles(target_keywords, max_profiles=30)
for profile in linkedin_profiles:
    print(profile)