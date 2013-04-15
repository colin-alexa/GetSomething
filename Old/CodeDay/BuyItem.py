#Hao Nguyen, John Yeung, Colin Robinson
from xml.dom import minidom
import ConfigParser, SendApiRequest
import sys

def BuyItem(token, itemID, maxBid):
	config = ConfigParser.ConfigParser()
	config.read("config.ini")

	request = "<?xml version='1.0' encoding='utf-8' ?>" +\
		"<PlaceOfferRequest xmlns='urn:ebay:apis:eBLBaseComponents'>" +\
		"<EndUserIP>0.0.0.0</EndUserIP>" +\
		"<BlockOnWarning>false</BlockOnWarning>" +\
		"<RequesterCredentials><eBayAuthToken>" + token + "</eBayAuthToken></RequesterCredentials>" +\
		"<ItemID>" + itemID + "</ItemID>"  +\
		"<Offer>" +\
			"<Action>Purchase</Action>" +\
			"<MaxBid>" + str(maxBid) + "</MaxBid>" +\
			"<Quantity>1</Quantity>" +\
			"<UserConsent>true</UserConsent>" +\
		"</Offer>" +\
		"</PlaceOfferRequest>"

	serverUrl = config.get("Server", "serverURL")

	respXml = SendApiRequest.SendApiRequest(request, serverUrl, "PlaceOffer")
	resp = minidom.parseString(respXml)

	if resp.getElementsByTagName("Ack")[0].firstChild.nodeValue == "Failure":
		return False
	
	return True
