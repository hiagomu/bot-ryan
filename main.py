import tweepy
import json
from time import sleep

consumer_key = 'CuG98BgJnaWMbNDeaWRNugZI2'
consumer_secret = 'B38SYWH5W51NUx0PiJo9iCciVA1z8G6gRGobDUjk5IApBgqazm'
access_token = '1250606030096084994-8JqJ8etj5jvjxrvpPDNK5XnuDSQfO6'
access_token_secret = 'VbleRoa77A61FXPsC9WqYlwcJj93VxTpldYITr5llI7ER'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
FILE_NAME = 'last_seen.txt'


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen = int(f_read.read().strip())
    f_read.close()
    return last_seen


def store_last_seen_id(last_seen, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen))
    f_write.close()
    return


def my_dict():
    json_arq = open('mydict.json', 'r')
    parsed_json = json.load(json_arq)
    new_dict = parsed_json['stats']
    json_arq.close()
    return new_dict


def search_n_update(new_dict, mention):
    for stats in new_dict:
        if stats['Player'].lower() in mention.full_text.lower().split():
            try:
                print(f'Maps Played: {stats["Maps"]}\nRating: {stats["Rating"]}')
                print('Respondendo...')
                api.update_status(
                    f'@{mention.user.screen_name} Player: {stats["Player"]}\nMaps: {stats["Maps"]}\nK/D: {stats["K/D"]}\nRating: {stats["Rating"]}',
                    mention.id)
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break


def search_mentions(mentions):
    for mention in reversed(mentions):
        print(f'{str(mention.id)} - {mention.full_text} - {mention.author.screen_name}')
        last_seen = mention.id
        store_last_seen_id(last_seen, FILE_NAME)
        new_dict = my_dict()
        search_n_update(new_dict, mention)


def reply_to_tweets():
    last_seen = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(
                        last_seen,
                        tweet_mode='extended')
    search_mentions(mentions)

while True:
    reply_to_tweets()
    sleep(20)
