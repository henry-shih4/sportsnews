import get_data
import pymongo_upload

url = f'https://api.foxsports.com/v2/content/optimized-rss?partnerKey=MB0Wehpmuj2lUhuRhQaafhBjAJqaPU244mlTDK1i&size=20&tags=fs/nba'

avoidList = ["|", "streaming", "odds", "standings", "betting", "mock", "tracker", "how to watch" ]






# JSON file containing the scraped data
json_file = 'NBA-article-data.json'

def get_NBA_articles():
    get_data.scrape(url,'NBA', avoidList)
    pymongo_upload.upload_to_mongodb(json_file)