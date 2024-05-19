import get_data
import pymongo_upload


url = f'https://api.foxsports.com/v2/content/optimized-rss?partnerKey=MB0Wehpmuj2lUhuRhQaafhBjAJqaPU244mlTDK1i&size=20&tags=fs/nfl'

avoidList = ["|", "streaming", "odds", "standings", "betting", "mock", "tracker", "how to watch" ]


# JSON file containing the scraped data
json_file = 'NFL-article-data.json'


def get_NFL_articles():
    get_data.scrape(url,'NFL', avoidList)
    pymongo_upload.upload_to_mongodb(json_file)