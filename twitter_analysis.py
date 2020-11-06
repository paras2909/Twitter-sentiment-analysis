import string
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import tweepy
from textblob import TextBlob
from re import sub

# Authentication
consumerKey = "s9fx1FEEviyRds0S2ImdAAlkw"
consumerSecret = "6K9HAahrdmqpnxRZhskJGnIopXXW3xpKHLP1YCmgr6KEsktEmG"
accessToken = "1160221780306354176-YlyqQLDhiNT4Bz8sN3W2xgbO40GFhH"
accessTokenSecret = "itwTs0k47ieiq2pM8eV7EgMzdZabjAZhifflFCr9yq1oD"

auth = tweepy.OAuthHandler(consumer_key=consumerKey, consumer_secret=consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

# Searching
searchTerm = input("Enter tweet subject to search for : ")
noOfSearchTerms = int(input("Enter the number of tweets to fetch : "))

tweets = api.search(q=searchTerm, count=noOfSearchTerms)
text_tweets = [[tweet.text] for tweet in tweets]

# Printing all Tweets
print("\nFetched Tweets :")
print(text_tweets)

text = ""
length = len(text_tweets)

# Converting all tweets into one string
for i in range(0,length):
    text = text_tweets[i][0] + " " + text

# Converting into lowercase.
lower_case = text.lower()

# Removing punctuations.
clean_text = lower_case.translate(str.maketrans('','',string.punctuation))

# Splitting sentences into words.
tokenized_words = word_tokenize(clean_text,"english")

# Removing words from tokenized words list which are present in "stop_words".
final_words = []
for word in tokenized_words:
    if word not in stopwords.words('english'):
        final_words.append(word)

emotion_list = []

# NLP Emotion Algorithm
    # 1. Check that word present in final_words list is also present in emotion.txt
    # 2. If word is present --> add emotion related to that word in emotion_list
    # 3. Count each emotion present in emotion_list
with open('emotions.txt','r') as file:
    for line in file:
        clear_line = line.replace('\n','').replace(',','').replace("'",'').strip()
        word, emotion = clear_line.split(':')

        if word in final_words:
            emotion_list.append(emotion)

print("\nEmotions :")
print(emotion_list)
w = Counter(emotion_list)
print(w)

# Counting tweets polarity wise
twat = []
srch = searchTerm
for strippin in tweets:
    texts = strippin.text
    analyze_text = ' '.join(sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+: / / \S+)", " ", texts).split())

    bob = TextBlob(analyze_text)
    textiment = {'text': texts, 'sentiment': bob.sentiment.polarity}

    if strippin.retweet_count:
        twat.append(textiment)
    else:
        if textiment not in tweets:
            twat.append(textiment)

def get_em(tweets):
    pos = []
    neg = []
    nut = []

    for a_tweet in tweets:
        if a_tweet['sentiment'] > 0:
            pos.append(a_tweet)
        elif a_tweet['sentiment'] < 0:
            neg.append(a_tweet)
        else:
            nut.append(a_tweet)

    get_per = lambda x: (noOfSearchTerms*(len(x)))/length

    if length==0:
        print('Sorry..!! Unable to find any tweets on the subject You Searched for')
    else:
        print("\nPolarity wise count of tweets :")
        print("Positive tweets: ", end=' ')
        try:
            print(round(get_per(pos)))
        except ZeroDivisionError:
            print(0)

        print("Negative tweets: ", end=' ')
        try:
            print(round(get_per(neg)))
        except ZeroDivisionError:
            print(0)

        print("Neutral tweets:  ", end=' ')
        try:
            print(round(get_per(nut)))
        except ZeroDivisionError:
            print(0)

get_em(twat)

# Counting Polarity
def sentiment_analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    neg = score['neg']
    pos = score['pos']
    neu = score['neu']
    compound = score['compound']

    print("\nPolarity :- ")
    print("Positive : ", pos)
    print("Negative : ",neg)
    print("Neutral  : ",neu)
    print("Compound : ",compound)

    if compound > 0:
        print("\nWe get Positive Vibes after analysing fetched tweets.")
    elif compound < 0:
        print("\nWe get Negative Vibes after analysing fetched tweets.")
    else:
        print("\nWe get Neutral Vibes after analysing fetched tweets.")

sentiment_analyse(clean_text)

# Barchart
fig, ax1 = plt.subplots()
ax1.bar(w.keys(),w.values())
fig.autofmt_xdate()
plt.xlabel("Emotion")
plt.ylabel("Count of Emotion")
plt.title("Emotion Counter")
plt.savefig('graph.png')
plt.show()

# Piechart
fig1 = plt.figure()
ax = fig1.add_axes([0,0,1,1])
ax.axis('equal')
emo = w.keys()
count = w.values()
ax.pie(count, labels=emo, autopct='%1.2f%%')
plt.savefig('piechart.png')
plt.show()