import get_data
import pymongo_upload


nfl_url = f'https://api.foxsports.com/v2/content/optimized-rss?partnerKey=MB0Wehpmuj2lUhuRhQaafhBjAJqaPU244mlTDK1i&size=20&tags=fs/nfl'

avoidList = ["|", "streaming", "odds", "standings", "betting", "mock", "tracker" ]


get_data.scrape(nfl_url,'NFL', avoidList)



# JSON file containing the scraped data
json_file = 'NFL-article-data.json'

pymongo_upload.upload_to_mongodb(json_file)