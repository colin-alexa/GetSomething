#Hao Nguyen, John Yeung, Colin Robinson
import urllib, json, random, sqlite3, os

# sub categories are not useful
file = None
def init_database():
    global file
    build = not os.path.exists('purchases.sqlite')
    file = sqlite3.connect('purchases.sqlite')
    file.row_factory = sqlite3.Row #so info is returned as dicts
    if build:
        cur = file.cursor()
        cur.execute("CREATE TABLE purchases (ID TEXT, url TEXT, category TEXT, UNIQUE(ID))")
        file.commit()

def getParent(categoryID):
    url = "http://open.api.ebay.com/Shopping?" +\
        "callname=GetCategoryInfo&" +\
        "version=677&" +\
        "appid=HaoNguye-e424-4914-99b4-4209afbb0a00&" +\
        "responseencoding=JSON&" +\
        "categoryID="+categoryID+"&" 

    resp = urllib.urlopen(url)
    r = resp.read()
    val = json.loads(r)
    parent = val['CategoryArray']['Category'][0]['CategoryParentID']
    if parent == '-1': actualParent = categoryID
    else: actualParent = getParent(parent)
    return actualParent

def save(item):
    global file
    cur = file.cursor()
    parent = getParent(item['primaryCategory'][0]['categoryId'][0])
    cur.execute("INSERT OR IGNORE INTO purchases VALUES (?, ?, ?)", (item['itemId'][0],item['viewItemURL'][0], parent))
    file.commit()

def purchases():
    '''Returns a list of lists. The first list represents all the database entries. If you want the most recent purchase,
    simply look at the end of the list. The lists in each list slot are purchases in the form ['itemId', 'url', 'category']'''
    global file
    cur = file.cursor()
    cur.execute("SELECT * FROM purchases")
    all = cur.fetchall()
    return all


def search(avoidCategory, maxPrice, feedbackMinimum, topSellersOnly = False):
    '''Takes an item name and searches for it, returning a TUPLE formed as such ([list of itemIDs],
    [list of actual items]). Takes (STRING avoidCategory, INT maxPrice, INT feedbackMinimum, BOOL topSellersOnly)'''
    categories = {'antiques':'20081', 'art':'550', 'baby':'2984','books':'267','business & industrial':'12576','cameras & photo':'625',
 'cell phones & accessories':'15032', 'clothing, shoes & accessories':'15032', 'coins & paper money':'1116',
 'collectibles':'1', 'computers/tablets & networking':'58058', 'consumer electronics': '293', 'crafts': '14439',
 'dolls & bears':'237', 'dvds & movies': '11232', 'entertainment memorabilia':'45100', 'everything else':'99',
 'gift cards & coupons':'172008', 'health & beauty':'26395', 'home & garden':'11700', 'jewelry & watches': '281',
 'music':'11233', 'musical instruments & gear':'619', 'pet supplies':'1281', 'pottery & glass':'870',
 'real estate':'10542', 'speciality services':'316', 'sporting goods':'382', 'sports mem, cards & fan shop':'64482',
 'stamps':'260', 'tickets':'1305', 'toys & hobbies':'220', 'travel':'3252', 'video games & consoles': '1249'}
    categoryString = avoidCategory
    while categoryString == avoidCategory:
       categoryString = random.choice(categories.keys())
    category = categories[categoryString]
    actualMaxPrice = str(maxPrice) + ".00"
    actualFeedbackMinimum = str(feedbackMinimum)
    if topSellersOnly: actualTopSellersOnly = 'true'
    else: actualTopSellersOnly = 'false'

    url = "http://svcs.ebay.com/services/search/FindingService/v1?" +\
        "OPERATION-NAME=findItemsByCategory&" +\
        "SERVICE-VERSION=1.9.0&" +\
        "SECURITY-APPNAME=HaoNguye-e424-4914-99b4-4209afbb0a00&" +\
        "RESPONSE-DATA-FORMAT=JSON&" +\
        "REST-PAYLOAD&" +\
        "categoryId="+category+"&" +\
        "itemFilter(0).name=AvailableTo&"+\
        "itemFilter(0).value=US&"+\
        "itemFilter(1).name=MaxPrice&" +\
        "itemFilter(1).value="+actualMaxPrice+"&" +\
        "itemFilter(1).paramName=Currency&" +\
        "itemFilter(1).paramValue=USD&" +\
        "itemFilter(2).name=TopRatedSellerOnly&" +\
        "itemFilter(2).value="+actualTopSellersOnly+"&" +\
        "itemFilter(3).name=FeedbackScoreMin"+\
        "itemFilter(3).value="+actualFeedbackMinimum+"&"+\
        "itemFilter(4).name=FreeShippingOnly"+\
        "itemFilter(4).value=true&"+\
        "itemFilter(5).name=ListingType&"+\
        "itemFilter(5).value=AuctionWithBIN&"

    resp = urllib.urlopen(url)
    r = resp.read()
    val = json.loads(r)
    results = val['findItemsByCategoryResponse'][0]['searchResult'][0]
    r = []
    r2 = []
    del results['@count']
    for item in results:
        for i in results[item]:
            r2.append(i)
            format = str(i['itemId']).strip('[').strip(']').strip('u').strip("'")
            r.append(format)
    final = (r, r2)
    if len(r) == 0: final = search(avoidCategory, maxPrice, feedbackMinimum, topSellersOnly)
    return final


#result = search('20081', 1, 0, True)
#result = search('20081', 1, 0, True)
#result = search('20081', 1, 0, False)
#save(result[1][0])
#pt = purchases()


