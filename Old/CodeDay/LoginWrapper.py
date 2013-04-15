#Hao Nguyen, John Yeung, Colin Robinson
import Login

loginInfo = Login.GetLoginPage()

f = open('buffer.txt', 'w')
f.write(loginInfo[1])
f.close()

#print out the loginPage
print loginInfo[0]