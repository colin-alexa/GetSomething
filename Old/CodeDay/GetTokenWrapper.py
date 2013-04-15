#Hao Nguyen, John Yeung, Colin Robinson
import Login
import sys, os

if os.path.exists('buffer.txt'):
	username = sys.argv[1]
	f = open('buffer.txt', 'r')
	sessionID = f.read()
	f.close()
	
	print Login.GetToken(username, sessionID)
else:
	print "false"
	



