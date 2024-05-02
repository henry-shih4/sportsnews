from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
import time
from pymongo_get_db import get_database
from datetime import datetime

def scrape(scrape_url, category, avoidList):
    dbname = get_database()
    collection_name = dbname["articles"]

    source = requests.get(scrape_url, headers={'User-Agent': 'Mozilla/5.0'})
    if source.status_code == 200:
        soup = BeautifulSoup(source.text, 'xml')
        
        articles = []
        items = soup.find_all('item')

        for item in items:
            article = {}
            title = item.find('title').text.strip()
            description = item.find('description').text.strip()
            skip = False
            for word in avoidList:
                if word in title or word in description:
                    skip = True
          
            article['title'] = title
            url = item.find('link').text
            if '/watch' in url:
                skip = True
            article['url'] = url
            if skip:
                continue
            query = {"title": title, "url": url}
            result = collection_name.find_one(query)
            if result:
                print('Article already exists in MongoDB')
                continue


            if url:
                # Start a Selenium webdriver
                driver=webdriver.Chrome()
                article_url = url
                # Load the page
                driver.get(article_url)
                # Wait for the dynamic content to load (adjust the sleep time as needed)
                time.sleep(5)
                # Get the page source
                html_content = driver.page_source
                # Parse the HTML content with BeautifulSoup
                soup2 = BeautifulSoup(html_content, "html.parser")
                # Find the elements you want
                contents = soup2.find_all(['p', 'h2', 'h3', 'ul', 'li'], class_=['article-content','ff-h'])
                article_content = ""
                for content in contents:
                    # if content.name == "li" or content.name == "ul":
                    #     article_content += " " + content.text + "\n"
                    # skip = False
                    # for link in content.find_all('a',href=True):
                    #     if "newsletter" or "FOX Sports" in link.text:
                    #         skip = True
                    # if skip:
                    #     continue
                    # else:
                        article_content +=  content.text + "\n"
                driver.quit()
            if article_content == "":
                continue
            article['content'] = article_content
            
            hero_img = item.find('media:content').get("url")
            thumbnail = item.find('media:thumbnail').get("url")
            date_written = item.find('pubDate').text
            
            article['description'] = description
            article['hero_img'] = hero_img
            article['thumbnail'] = thumbnail
            article['category'] = category
            article['date'] = date_written
            article['comments'] = []
            
            articles.append(article)
        
        try:
            with open(category +'-article-data' +'.json', 'r') as f:
                existing_data = json.load(f)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            existing_data = []
        for article in articles:
            if article not in existing_data:
                existing_data.append(article)
        # save updated data to JSON file
        with open(category +'-article-data' +'.json', "w") as f:
            json.dump(existing_data, f)

        print("Data saved to " + category +"-article-data" +".json file.")
    else:
        print("Failed to retrieve data from the RSS feed.")


