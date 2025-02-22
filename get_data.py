from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pymongo_get_db import get_database
from datetime import datetime
import chromedriver_autoinstaller
from selenium.common.exceptions import WebDriverException
import datetime
from markdownify import markdownify as md


def scrape(scrape_url, category, avoidList):
    chromedriver_autoinstaller.install() 

    options = Options()    
    # Add your options as needed    
    # options = [
    # "--no-sandbox",
    # "--window-size=1200,1200",
    #     "--ignore-certificate-errors"
    #     "--headless",
    #     #"--disable-gpu",
    #     #"--window-size=1920,1200",
    #     #"--ignore-certificate-errors",
    #     #"--disable-extensions",
    #     #"--disable-dev-shm-usage",
    # #'--remote-debugging-port=9222'
    # ]

    options.add_argument('--headless')

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
            query = {"url": url}
            result = collection_name.find_one(query)
            if result:
                print('Article already exists in MongoDB')
                continue
            
            
            if url:
                try:
                    # Start a Selenium webdriver
                    driver=webdriver.Chrome(options = options)
                    article_url = url
                    # Load the page
                    driver.get(article_url)
                    # Wait for the dynamic content to load (adjust the sleep time as needed)
                    time.sleep(5)
                    # Get the page source
                    html_content = driver.page_source
                    # Parse the HTML content with BeautifulSoup
                    soup2 = BeautifulSoup(html_content, "html.parser")
                    soup2.a.decompose()

                    for a in soup2.find_all('a'):
                        a.replace_with(a.get_text())
                    # Find the elements you want
                    contents = soup2.find_all(['p', 'h2', 'h3', 'ul', 'li'], class_=['article-content','ff-h'])
                    article_content = ""
                    skip = 'FOX Sports account'
                    for content in contents:
                        text = str(content)
                        if skip in text:
                            continue
                        article_content += (text)
                except WebDriverException as e:
                    print("An error occurred:", e)
                finally:
                    # Close the WebDriver
                    driver.quit()
            if article_content == "":
                continue

            markdown_content = md(article_content, heading_style="ATX")

            article['content'] = markdown_content
            
            hero_img = item.find('media:content').get("url")
            thumbnail = item.find('media:thumbnail').get("url")
            date_written = item.find('pubDate').text
            
            article['description'] = description
            article['hero_img'] = hero_img
            article['thumbnail'] = thumbnail
            article['category'] = category
            article['date'] = date_written
            article['date_upload'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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


