import requests
from bs4 import BeautifulSoup
import time
import csv

#create a list of keywords for the study
covid_words = ["Covid-19", "coronavirus", "pandemic"]
keywords = ["freedom", "rights", "liberty", "choice", "autonomy", "self-determination", "sovereignty", "independence"]

 # idenetify target url for crawling 
url = 'https://rnz.co.nz/search/results?page=470&q=covid-19'

 # create a CSV file and write the header row
with open('radioNZ_articles.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['date', 'heading', 'body'])

    #create  a variable which remains false until the last page of the archive is reached
    last_page = False

    # create a while loop which executes until the last page of the archive is reached
    while not last_page:

        current_url = url

        # request the page with list of URLs you want to crawl
        response = requests.get(current_url)
        print(f"current url: {current_url}")

        # create a BeautifulSoup object
        soup = BeautifulSoup(response.text, 'html.parser')

        # select the links you want to crawl
        links = soup.select('a.faux-link')
        next_button = soup.select_one('.next a')

        # select the next button at bottom of page and save url for next loop
        next_url = 'https://rnz.co.nz' + next_button['href']
        print(f"next url {next_url}")

        if links:
            print(f"Number of links found: {len(links)}")
        else:
            print("ERROR, no links found")
            break

        # iterate over the links
        for link in links:

            # construct a full url for each story
            article_url = 'https://rnz.co.nz' + link['href']
            print(f"article url: {article_url}")

            # request the story page url
            article_response = requests.get(article_url)

            # create a BeautifulSoup object for the story page
            article_soup = BeautifulSoup(article_response.text, 'html.parser')

            if (article_soup.select_one('h1') and article_soup.select_one('span.updated') and article_soup.select_one('.article__body')):

                # select the content you want
                heading = article_soup.select_one('h1')
                date = article_soup.select_one('span.updated')
                body = article_soup.select_one('.article__body')
                
                # get the text from the body, date, and heading elements
                body_text = body.get_text()
                heading_text = heading.get_text()
                date_text = date.get_text()

                # create list of words to check for keywords
                heading_words = heading_text.split()
                body_words = body_text.split()

                # if keyword in the body or heading og the article, extract text and save as csv
                keyword_check =  any(word in keywords for word in body_words or (word in keywords for word in heading_words))
                covid_check =  any(word in covid_words for word in body_words or (word in covid_words for word in heading_words))
                
                print(f"relevant article located: {keyword_check and covid_check}")

                if keyword_check and covid_check:

                    # write the data to the CSV file
                    writer.writerow([date_text, heading_text, body_text])

            # pause for a moment - it is a good idea to give the server a rest
            time.sleep(2)

        # if there is a next button on the page, update url to next page otherwise termuinate while loop by updating nex_page variable to "True"
        if next_button:
            url = next_url

        # otherwise end while loop by changing boolean to "True"
        else:
            last_page = True

