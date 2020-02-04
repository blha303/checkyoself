#!/usr/bin/env python3

import twitter
from json import load

with open("t.json") as f:
    api = twitter.Api(**load(f))

# https://github.com/bear/python-twitter/blob/master/examples/get_all_user_tweets.py
def get_timeline(screen_name):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            timeline += tweets

    return timeline

def get_bad_words_from_timeline(username):
    timeline = get_timeline(username)
    with open("badwords.txt") as f:
        badwords = f.read().splitlines()
    for tweet in timeline:
        if any(word in tweet.text for word in badwords):
            yield tweet

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("username")
    args = parser.parse_args()

    for tweet in get_bad_words_from_timeline(args.username):
        print("https://twitter.com/{}/status/{}\n  {}".format(args.username, tweet.id, tweet.text))

    return 0

if __name__ == "__main__":
    from sys import exit
    exit(main())
