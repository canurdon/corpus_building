import requests
from bs4 import BeautifulSoup
import time
import csv

#create a list of keywords for the study
keywords = ["freedom", "rights", "liberty", "choice", "autonomy", "self-determination", "sovereignty", "agency", "independence"]

#create  a variable which remains false until the last page of the archive is reached
last_page = False

 # idenetify target url for crawling 
url = 'https://www.rnz.co.nz/search/results?q=covid-19&commit=Search'

# create a while loop which executes until the last page of the archive is reached
while not last_page:

    # request the page with list of URLs you want to crawl
    response = requests.get(url)
    print(url)

    # create a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # select the links you want to crawl
    links = soup.select('a.faux-link')
    next_button = soup.select_one('.next a')

    # select the next button at bottom of page and save url
    next_url = 'https://rnz.co.nz' + next_button['href']
    print(next_url)

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
            url = 'https://rnz.co.nz' + link['href']
            print(url)

            # request the story page url
            story_response = requests.get(url)

            # create a BeautifulSoup object for the story page
            story_soup = BeautifulSoup(story_response.text, 'html.parser')

            if (story_soup.select_one('h1') and story_soup.select_one('span.updated') and story_soup.select_one('.article__body')):

                # select the content you want
                heading = story_soup.select_one('h1')
                date = story_soup.select_one('span.updated')
                body = story_soup.select_one('.article__body')
                
                # get the text from the body, date, and heading elements
                body_text = body.get_text()
                heading_text = heading.get_text()
                date_text = date.get_text()

                # create list of words to check for keywords
                heading_words = heading_text.split()
                body_words = body_text.split()

                # if keyword in the body or heading og the article, extract text and save as csv
                keyword_check =  any(word in keywords for word in body_words or (word in keywords for word in heading_words))
                
                print(f"relevant article located: {keyword_check}")

                if keyword_check:

                    # write the data to the CSV file
                    writer.writerow([date_text, heading_text, body_text])

            # pause for a moment - it is a good idea to give the server a rest
            time.sleep(2)
    
    # if there is a next button on the page, update url to next page otherwise termuinate while loop by updating nex_page variable to "True"
    if next_button:
        url = next_url
    
    else:
        last_page = True

