#Hao Nguyen, John Yeung, Colin Robinson
import urllib, json, random, sqlite3, os

categories = {'antiques':'20081', 'art':'550', 'baby':'2984','books':'267','business & industrial':'12576','cameras & photo':'625',
 'cell phones & accessories':'15032', 'clothing, shoes & accessories':'15032', 'coins & paper money':'1116',
 'collectibles':'1', 'computers/tablets & networking':'58058', 'consumer electronics': '293', 'crafts': '14439',
 'dolls & bears':'237', 'dvds & movies': '11232', 'entertainment memorabilia':'45100', 'everything else':'99',
 'gift cards & coupons':'172008', 'health & beauty':'26395', 'home & garden':'11700', 'jewelry & watches': '281',
 'music':'11233', 'musical instruments & gear':'619', 'pet supplies':'1281', 'pottery & glass':'870',
 'real estate':'10542', 'speciality services':'316', 'sporting goods':'382', 'sports mem, cards & fan shop':'64482',
 'stamps':'260', 'tickets':'1305', 'toys & hobbies':'220', 'travel':'3252', 'video games & consoles': '1249'}


picked = {'everything else': 1, 'art': 1, 'pet supplies': 1, 'cell phones & accessories': 1, 'books': 1, 'gift cards & coupons': 1,
          'sporting goods': 1, 'cameras & photo': 1, 'video games & consoles': 1, 'dolls & bears': 1, 'business & industrial': 1,
          'collectibles': 1, 'travel': 1, 'antiques': 1, 'dvds & movies': 1, 'stamps': 1, 'musical instruments & gear': 1, 'music': 1, 
          'clothing, shoes & accessories': 1, 'real estate': 1, 'sports mem, cards & fan shop': 1, 'home & garden': 1, 'coins & paper money': 1,
          'health & beauty': 1, 'baby': 1, 'tickets': 1, 'consumer electronics': 1, 'computers/tablets & networking': 1, 'toys & hobbies': 1,
          'entertainment memorabilia': 1, 'crafts': 1, 'jewelry & watches': 1, 'pottery & glass': 1, 'speciality services': 1}

# sub categories are not useful
file = None
def init_database():
    global file
    build = not os.path.exists('LivePurchases.sqlite')
    file = sqlite3.connect('LivePurchases.sqlite')
    file.row_factory = sqlite3.Row #so info is returned as dicts
    if build:
        cur = file.cursor()
        cur.execute("CREATE TABLE purchases (ID TEXT, url TEXT, category TEXT, UNIQUE(ID))")
        cur.execute("CREATE TABLE categories (category TEXT, picked INT, unique(category))")
        cur.executemany("INSERT INTO categories VALUES (?,?)", picked.items())
        file.commit()
    else:
        cur = file.cursor()
        cur.execute("SELECT * FROM CATEGORIES")
        populate = cur.fetchall()
        for item in populate:
            #print item[0] + " = " +str(item[1])
            picked[item[0]] = item[1]

        pass

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


def search(maxPrice, feedbackMinimum, topSellersOnly = False):
    '''Takes an item name and searches for it, returning a TUPLE formed as such ([list of itemIDs],
    [list of actual items]). Takes (INT maxPrice, INT feedbackMinimum, BOOL topSellersOnly)
    Given that this method only produces a list, it is strongly suggested to use Find instead'''

    #perhaps take a min price; or set min price to half of price when the amount they give us >$10

    #categoryString = random.choice(categories.keys())
    #Weighted Random ala http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice

    offset = random.randint(0, sum(picked.itervalues())-1)
    for k, v in picked.iteritems():
        if offset < v:
            categoryString = k
        offset -= v
    picked[categoryString] = picked[categoryString]+1
    global file
    cur = file.cursor()
    cur.execute("UPDATE categories SET picked=? WHERE category=?", (picked[categoryString], categoryString))
    file.commit()
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


