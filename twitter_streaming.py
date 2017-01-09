import tweepy
import os
import datetime
import json

# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
track = ['News']

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    count = 0
    filename = str(datetime.datetime.now())
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s\n' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        # print ''
        # print data + '\n'
        
        directory = ' '.join(track)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        
        
        targetFile = open(directory + '/' + StdOutListener.filename, 'a')
        targetFile.write(data + '\n')
        targetFile.close()

        StdOutListener.count += 1
        
        if StdOutListener.count == 10:
            StdOutListener.filename = str(datetime.datetime.now())
            StdOutListener.count = 0
        
        return True

    def on_error(self, status):
        print 'Error:' + status

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    if len(track) == 0:
        print 'Error: Enter atleast one keyword to track.'
    else:
        print "Showing all new tweets for %s:" % track
        while True:
            try:
                stream = tweepy.Stream(auth, l)
                stream.filter(track=track)
            except KeyboardInterrupt:
                raise
            except:
                print str(datetime.datetime.now()) + ' Exception found and ignored.'
