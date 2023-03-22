import requests
from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# identify target URL
url = 'https://www.nytimes.com/search?dropmab=false&endDate=20230321&query=covid-19&sort=best&startDate=20200101'

#create a list of keywords for the study
covid_ids = ["Covid-19", "coronavirus"]
keywords = ["freedom", "rights", "liberty", "choice", "autonomy", "self-determination", "sovereignty", "agency", "independence"]

# Set up Chrome webdriver
driver = webdriver.Chrome()

# Navigate to target URL
driver.get(url)

# Define function to check if "show more" button is present
def is_show_more_present():
    try:
        show_more_button = driver.find_element_by_xpath('//*[@id="site-content"]/div/div[2]/div[3]/div/button')
        return show_more_button.is_displayed()
    except:
        return False

# Loop until "show more" button is no longer present
while is_show_more_present():
    # Click "show more" button
    show_more_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[2]/div[3]/div/button')))
    show_more_button.click()

# All data should now be loaded

# use Selenium driver to create variable containing html of entire archive
html_source = driver.page_source
print(html_source)
break
# request the page with list of URLs you want to crawl
response = requests.get(html_source)

# create a BeautifulSoup object
soup = BeautifulSoup(response.text, 'html.parser')

# select the links you want to crawl
links = soup.select('.css-1l4w6pd a')

if links:
    print(f"Number of links found: {len(links)}")
else:
    print("ERROR, no links found")

# create a CSV file and write the header row
with open('radioNZ_articles.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['date', 'heading', 'body'])

    # iterate over the links
    for link in links:

        # construct a full url for each story
        url = 'https://www.nytimes.com/' + link['href']
        print(url)

        # request the story page url
        story_response = requests.get(url)

        # create a BeautifulSoup object for the story page
        story_soup = BeautifulSoup(story_response.text, 'html.parser')

        # select the content you want
        heading = story_soup.select_one('h1')
        date = story_soup.select_one('span.css-1sbuyqj')
        body = story_soup.select_one('.css-at9mc1 evys1bk0')

        # get the text from the body, date, and heading elements
        body_text = body.get_text()
        heading_text = heading.get_text()
        date_text = date.get_text()

        # create list of words to check for keywords
        heading_words = heading_text.split()
        body_words = body_text.split()

        # if keyword in the body or heading og the article, extract text and save as csv
        covid_check = any(word in covid_ids for word in body_words) or any(word in covid_ids for word in heading_words)
        keyword_check =  any(word in keywords for word in body_words) or (word in keywords for word in heading_words)
        
        print(f"relevant article located: {keyword_check and covid_check}")

        if covid_check and keyword_check:

            # write the data to the CSV file
            writer.writerow([date_text, heading_text, body_text])

        # pause for a moment - it is a good idea to give the server a rest
        time.sleep(2)
