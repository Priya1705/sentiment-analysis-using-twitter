import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
  
class TwitterClient(object): 
    def __init__(self): 
        consumer_key = 'tyjMoohm9m9iqLkuNw9PqiG3J'
        consumer_secret = 'iqSS77j6zJ7OuNK4enanTMba0Prqw9wkQxKstHPKsh33bXSiEb'
        access_token = '886678689282367488-iHe6uF9hv0kZJjufxYUGFshUfApq5Ex'
        access_token_secret = 'TTW38MJJ5w4VAvH8URhhqQD2TP5j5GLN6VICVpCnHiwt9'

        try: 
            self.auth = OAuthHandler(consumer_key, consumer_secret)  
            self.auth.set_access_token(access_token, access_token_secret)  
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        tweets = [] 
  
        try: 
            fetched_tweets = self.api.search(q = query, count = count)
            for tweet in fetched_tweets: 
                parsed_tweet = {} 
                parsed_tweet['text'] = tweet.text 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
            return tweets 
  
        except tweepy.TweepError as e:
            print("Error : " + str(e)) 
  
def main(): 
    api = TwitterClient() 
    tweets = api.get_tweets(query = 'Donald Trump', count = 200) 
  
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    p=(len(ptweets)/len(tweets))*100
    print("Positive tweets percentage: {} %".format(p))
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 

    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]: 
        print(tweet['text']) 

    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text']) 
  
if __name__ == "__main__": 
    main() 