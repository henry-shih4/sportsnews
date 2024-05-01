import get_data
import pymongo_upload

url = f'https://api.foxsports.com/v2/content/optimized-rss?partnerKey=MB0Wehpmuj2lUhuRhQaafhBjAJqaPU244mlTDK1i&size=20&tags=fs/nba'

avoidList = ["|", "streaming", "odds", "standings", "betting", "mock", "tracker" ]


get_data.scrape(url,'NBA', avoidList)


# if ('|' in title) or ('streaming' in title) or ('odds' in title) or ('standings' in title) or ('betting' in title) or ('mock' in title or 'tracker' in title):


# JSON file containing the scraped data
json_file = 'NBA-article-data.json'

pymongo_upload.upload_to_mongodb(json_file)