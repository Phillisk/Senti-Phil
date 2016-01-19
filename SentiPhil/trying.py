import sys
from PyQt4 import QtGui, QtCore
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sentiment_mod as s

#consumer key, consumer secret, access token, access secret.
ckey="MHcwkVAz8ddKR7LzAOinopuNZ"
csecret="cizui5BKeCKsuA06UNlcpHuBf06Jz5mwRBETP40EmwL5xrR5Cl"
atoken="500688534-29zVrFfXJ74HnyIUoKtVDZpJFMyTpl0n1qgbmpxz"
asecret="08UZXWtBUan5zkWAy6tA9yKkNy1klD9fCYHb2xXau0AIj"


class listener(StreamListener):

    def on_data(self, data):

            all_data = json.loads(data)

            tweet = all_data["text"]
            sentiment_value, confidence = s.sentiment(tweet)
            print(tweet, sentiment_value, confidence)

            if confidence*100 >= 80:

                    output = open("twitter-out.txt","a")
                    output.write(sentiment_value)
                    output.write('\n')
                    output.close()

            return True

    def on_error(self, status):
        
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

class SearchTerm(QtGui.QWidget):
	def __init__(self):
		super(SearchTerm, self).__init__()
		self.initUI()

	def initUI(self):
		self.resize(700,650)
		self.setWindowTitle('Twitter Search. Enter the key word to search!')
		self.home()

	def home(self):
		self.btn = QtGui.QPushButton('Search', self)
		self.btn.clicked.connect(self.searchParams)
		self.btn.move(100,30)
		self.search_field = QtGui.QLineEdit(self)
		self.label = QtGui.QLabel("Results",self)
		self.label1 = QtGui.QLabel("Query",self)
		self.label.move(0,200)
		self.label1.move(0,180)
		self.show()

	def searchParams(self):
		text = self.search_field.text()
		self.label1.setText("You Searched for "+text+ " on twitter")
		self.label1.adjustSize()
		
		finalValues = twitterStream.filter(track=[text])
		self.label.setText(finalValues)
		
		self.label.adjustSize()
		

def main():
	app = QtGui.QApplication(sys.argv)
	ex = SearchTerm()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
