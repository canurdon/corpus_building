import requests
from bs4 import BeautifulSoup
import time
import csv
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


# create function to load all pages for given url
def load_articles(keywords, covid_ids):

    # ask the user to input the search results page from the NYT that they would like to scrape
    url = input("Enter the NYT search page URL you would like to scrape: ")

    # create variable for path to web driver and create driver object
    chrome_path = r"/Users/duncanoregan/Desktop/chromedriver_mac64/chromedriver"
    service = Service(chrome_path)
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(3)

    # create list object to store the links that are collected from the url
    links = []
    
    # create a counter to count the number of scraped articles
    article_counter = 0

    # create boolean to reflect whether all the paegs have been loaded
    pages_loaded = False

    # load each page and scrape relevant text
    while not pages_loaded:

        try:

            # use the Selenium driver to click the load more button
            show_more = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.css-vsuiox button')))
            driver.execute_script("arguments[0].click();", show_more)
            time.sleep(2)

            # use Selenium driver to extract URLs and store in the new_links list
            new_links = driver.execute_script("return Array.from(document.querySelectorAll('.css-1l4w6pd a')).map(a => a.href)")

            # for each link in the new_links list, check if new_links are already in the links list - if not go to the link and see if its text is relevant
            for link in new_links:

                if link not in links:
                    
                    print(link)

                    # create headers for request
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # request the story page url
                    story_response = requests.get(link, headers=headers)

                    # create a BeautifulSoup object for the story page
                    story_soup = BeautifulSoup(story_response.text, 'html.parser')

                    # select the content you want
                    heading = story_soup.select_one('h1')
                    date = story_soup.select_one('time')
                    paragraphs = story_soup.select('.css-53u6y8') 
                    
                    #if the article does not have a date, a heading, and at least one paragraph, move to next article
                    if not (heading and date and paragraphs):
                        links.append(link)
                        continue 

                    # get the text from the body element
                    body_text = ''

                    for p in paragraphs:
                        body_text += p.get_text()

                    # get the text from the date and heading elements
                    heading_text = heading.get_text()
                    date_text = date.get_text()

                    # create list of words to check for keywords
                    heading_words = heading_text.split()
                    body_words = body_text.split()

                    # if keyword in the body or heading og the article, extract text and save as csv
                    covid_check = any(word in covid_ids for word in body_words) or any(word in covid_ids for word in heading_words)
                    keyword_check =  any(word in keywords for word in body_words) or any(word in keywords for word in heading_words)
                    
                    print(f"relevant article located: {keyword_check and covid_check}")

                    if covid_check and keyword_check:

                        # create directory path variable
                        directory_path = "/Users/duncanoregan/Desktop/UCdatascience/DIGI405/Assignments/corpus_building/NYT"

                        #create file name
                        file_name = f"nyt_{date_text}"

                        # open .txt file
                        with open(os.path.join(directory_path, f'{file_name}.txt'), 'w') as f:
                            f.write(heading_text)
                            f.write("\n")
                            f.write(body_text)

                        article_counter += 1
                        print(f"number of articles scraped: {article_counter}")

                    # pause for a moment - it is a good idea to give the server a rest
                    time.sleep(2)

                    #append link to list of processed links
                    links.append(link)
        
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            print("Retrying in 10 seconds...")
            time.sleep(10)
            continue 
        
    print(f"Show more button clicked - {len(links)} links extracted")
    print(f"number of articles scraped: {article_counter}")
    
    return links, article_counter

#create a list of keywords for the study
covid_words_list = ["Covid-19", "coronavirus"]
keywords_list = ["freedom", "rights", "liberty", "choice", "autonomy", "self-determination", "sovereignty", "independence"]

# load all pages from target url
links, article_counter = load_articles(keywords_list, covid_words_list)