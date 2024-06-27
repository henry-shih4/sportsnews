from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import chromedriver_autoinstaller
from selenium.common.exceptions import WebDriverException
from markdownify import markdownify as md



chromedriver_autoinstaller.install() 

options = Options()    


options.add_argument('--headless')

url = "https://www.foxsports.com/stories/nfl/49ers-wr-brandon-aiyuk-trade-destinations-steelers-commanders-top-list"
article_content = ''

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
    skip = 'FOX Sports account'
    for content in contents:
        text = str(content)
        if skip in text:
            continue
        article_content += (text)

    
    

    # print(h)
        # article_content += (str(content)) 

    markdown_content = md(article_content, heading_style="ATX")
    
    print(markdown_content)

except WebDriverException as e:
    print("An error occurred:", e)
finally:
    # Close the WebDriver
    driver.quit()
