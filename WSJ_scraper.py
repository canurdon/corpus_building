import requests
from bs4 import BeautifulSoup
import time
import csv
import os

#create a counter to keep track of how many articles have been scraped
scraped_articles = 0

#create a list of keywords for the study
covid_words = ["Covid-19", "coronavirus", "pandemic"]
keywords = ["freedom", "rights", "liberty", "choice", "autonomy", "self-determination", "sovereignty", "independence"]

 # idenetify target url for crawling 
url = "https://www.wsj.com/search?query=covid-19&isToggleOn=true&operator=OR&sort=relevance&duration=1y&startDate=2020%2F01%2F01&endDate=2020%2F12%2F31&source=wsjie%2Cblog%2Cwsjvideo%2Cinteractivemedia%2Cwsjsitesrch%2Cwsjpro%2Cwsjaudio%2Clivecoverage"

#create  a variable which remains false until the last page of the archive is reached
last_page = False

# create a while loop which executes until the last page of the archive is reached
while not last_page:

    # print total number of scraped articles
    print(f"number of articles scraped: {scraped_articles}")

    # create variable to store url being crawled for links
    current_url = url

    # create some headers for the request to prevent being identified as a bot
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # request the page with list of URLs you want to crawl
    response = requests.get(current_url, headers)
    print(f"current url: {current_url}")

    # create a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # select the links you want to crawl

    #save article links
    links = soup.select('.WSJTheme--headline--7VCzo7Ay a')
    
    # save next button
    next_button = soup.select_one('.WSJTheme--button--12LOad_- typography--sans-serif--1WZesAGA WSJTheme--pagination--3MTI0FnK WSJTheme--next--2r7-j2I8')

    # select the next button at bottom of page and save url for next loop
    next_url = next_button['href']
    print(f"next url {next_url}")

    if links:
        print(f"Number of links found: {len(links)}")
    else:
        print("ERROR, no links found")

    # iterate over the links
    for link in links:

        # construct a full url for each story
        article_url = link['href']
        print(f"article url: {article_url}")

        # request the story page url
        article_response = requests.get(article_url, headers)

        # create a BeautifulSoup object for the story page
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        if (article_soup.select_one('h1') and article_soup.select_one('.author__info time') and article_soup.select_one('.article__body p')):

            # select the content you want
            heading = article_soup.select_one('h1')
            date = article_soup.select_one('time')
            paragraphs = article_soup.select('.css-xbbvutc-Paragraph')

            # collect body text from paragraphs array
            body_text = ''
            
            for p in paragraphs:
                body_text += p.get_text()
            
            # get the text from the body, date, and heading elements
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

                # write the data to a txt file
                
                # create directory path variable
                directory_path = "/Users/duncanoregan/Desktop/UCdatascience/DIGI405/Assignments/corpus_building/WSJ"

                #create file name
                file_name = f"WSJ_{date_text}"

                # open .txt file
                with open(os.path.join(directory_path, f'{file_name}.txt'), 'w') as f:
                    f.write(heading_text)
                    f.write("\n")
                    f.write(body_text)

                # update counter variable
                scraped_articles += 1
        
        # pause for a moment - it is a good idea to give the server a rest
        time.sleep(2)

    # if there is a next button on the page, update url to next page otherwise termuinate while loop by updating nex_page variable to "True"
    if next_button:
        url = next_url

    # otherwise end while loop by changing boolean to "True"
    else:
        last_page = True

