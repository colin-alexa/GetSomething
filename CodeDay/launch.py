#Hao Nguyen, John Yeung, Colin Robinson
import FindItems as p
import random, sys
import BuyItem

maxPrice = sys.argv[1]
token = sys.argv[2]

p.init_database()

purchases = p.purchases()
purchasesLength = len(purchases)
if purchasesLength != 0:
    purchase = purchases[purchasesLength-1]
    result = p.search(purchase[2], maxPrice, 0, False)
else:
    result = p.search('10542', maxPrice, 0, False)
	
index = random.randint(0, len(result))
BuyItem.BuyItem(token, result[0][index], result[1][index]['sellingStatus'][0]['currentPrice'][0]['__value__'])
p.save(result[1][index])

print result[1][index]['viewItemURL'][0]


