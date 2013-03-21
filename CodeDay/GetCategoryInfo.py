#Hao Nguyen, John Yeung, Colin Robinson
from xml.dom import minidom
import ConfigParser, SendApiRequest, Login

def GetCategoryInfo(catID):
	config = ConfigParser.ConfigParser()
	config.read("config.ini")
	
	shoppingUrl = config.get("Server", "shoppingURL")

	request = "<?xml version='1.0' encoding='utf-8' ?>" +\
		"<GetCategoryInfoRequest xmlns='urn:ebay:apis:eBLBaseComponents'>" +\
			"<CategoryID>" + catID + "</CategoryID>"+\
		"</GetCategoryInfoRequest>"
	
	respXml = SendApiRequest.SendApiRequest(request, shoppingUrl, "GetCategoryInfo")
#	resp = minidom.parseString(respXml)

	print respXml


def GetCategories(token):
	config = ConfigParser.ConfigParser()
	config.read("config.ini")
	
	serverUrl = config.get("Server", "serverURL")
	
	request = "<?xml version='1.0' encoding='utf-8' ?>" +\
		"<GetCategoriesRequest xmlns='urn:ebay:apis:eBLBaseComponents'>" +\
			"<RequesterCredentials><eBayAuthToken>" + token + "</eBayAuthToken></RequesterCredentials>" +\
			"<CategorySiteID>0</CategorySiteID>" +\
			"<DetailLevel>ReturnAll</DetailLevel>" +\
		"</GetCategoriesRequest>"

	respXml = SendApiRequest.SendApiRequest(request, serverUrl, "GetCategories")
	
	return  respXml

#testing
loginInfo = Login.GetLoginPage()
sessionID = loginInfo[1]
loginPage = loginInfo[0]

GetCategoryInfo("1466")
