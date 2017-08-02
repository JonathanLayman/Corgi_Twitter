import twitter
import urllib.request
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import date, timedelta
import random
from settings import *

# Twitter API setup
api = twitter.Api(consumer_key=ckey, consumer_secret=csecret, access_token_key=atoken, access_token_secret=asecret)
yesterday = (date.today() - timedelta(1)).strftime('%Y-%m-%d')
result = api.GetSearch(term='Corgi', count=100, lang='en', since=yesterday)
corgi_pics = []
final_tweet = ''


def send_mail(img_file_name):
    img_data = open(img_file_name, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = random.choice(subjects)
    msg['From'] = from_addr
    msg['To'] = to_addr

    text = MIMEText(random.choice(content))
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(img_file_name))
    msg.attach(image)

    s = smtplib.SMTP(smtp_gmail)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(username, password)
    s.sendmail(from_addr, to_addr, msg.as_string())
    s.quit()


# get list of urls for pictures of corgis
for tweet in result:
    tweet = tweet.AsDict()
    if 'media' in tweet and tweet['media'][0]['type'] == 'photo':
        if 'retweet_count' in tweet:
            corgi_pics.append(tweet)

# find the highest amount of retweets
retweets = max([retweet_count['retweet_count'] for retweet_count in [tweet for tweet in corgi_pics]])

# find the tweet that matches the highest number
for tweet in corgi_pics:
    if tweet['retweet_count'] == retweets:
        final_tweet = tweet['media'][0]['media_url']

urllib.request.urlretrieve(final_tweet, 'daily_corgi.jpg')

send_mail('daily_corgi.jpg')
