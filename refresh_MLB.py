import get_data
import pymongo_upload


url = f'https://api.foxsports.com/v2/content/optimized-rss?partnerKey=MB0Wehpmuj2lUhuRhQaafhBjAJqaPU244mlTDK1i&size=30&tags=fs/mlb'

avoidList = ["|", "Ben Verlander", "streaming", "odds", "standings", "betting", "mock", "tracker" ]





# JSON file containing the scraped data
json_file = 'MLB-article-data.json'



def get_MLB_articles():
    get_data.scrape(url,'MLB', avoidList)
    pymongo_upload.upload_to_mongodb(json_file)