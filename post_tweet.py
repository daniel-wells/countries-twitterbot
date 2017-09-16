import tweepy
import configparser
import requests
import os
import json
import dateutil.parser
import random

def twitter_api():
    access_token = config.get('twitter', 'access_token')
    access_token_secret = config.get('twitter', 'access_token_secret')
    consumer_key = config.get('twitter', 'consumer_key')
    consumer_secret = config.get('twitter', 'consumer_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def post_tweet(messages, images, coordinates):
    api = twitter_api()
    
    # first tweet contains message and flag image
    media_ids = [api.media_upload(images[0]).media_id_string] # for i in image
    status = api.update_status(status=messages[0], media_ids=media_ids, lat=coordinates[1], long=coordinates[0])
    
    # second tweet (in reply to original) contains map image
    media_ids = [api.media_upload(images[1]).media_id_string]
    api.update_status(status=messages[1], media_ids=media_ids, in_reply_to_status_id=status.id, lat=coordinates[1], long=coordinates[0])


def create_tweet(result):
    popDate = str(dateutil.parser.parse(result["popDate"]["value"]).year)

    coordinates = result["coordinate"]["value"]
    coordinates = coordinates.replace("Point(","")
    coordinates = coordinates.replace(")","")
    coordinates = coordinates.split(" ")
    coordinates = [float(i) for i in coordinates]
    
    # if there's a capital
    if result["capitalLabels"]["value"]:
        if "," in result["capitalLabels"]["value"]:
            capitaltext = "\nCapital(s): " + result["capitalLabels"]["value"]
        else:
            capitaltext = "\nCapital: " + result["capitalLabels"]["value"]
    else:
        capitaltext = ""
    
    # if the population has a date of estimation
    if popDate:
        popDatetext = " (" + popDate + ")"
    else:
        popDatetext = ""
    
    # compile message
    message = (result["countryLabel"]["value"] +
                capitaltext +
                "\nPopulation: " +
                format(int(result["population"]["value"]), ",d") +
                popDatetext)
    
    # Second message is just emoji
    messages = [message, result["emoji"]["value"]]
    
    images = ('images/' + result["countryLabel"]["value"] + '_' + 'flag' + '.png',
            'images/' + result["countryLabel"]["value"] + '_' + 'map' + '.png')
    
    return(messages, images, coordinates)


# Import our Twitter credentials from credentials.ini
config = configparser.ConfigParser()
config.read('credentials.ini')

# Load data
results = json.load(open('data.json'))

# Choose a random country and tweet it
random.shuffle(results["results"]["bindings"])

def lambda_handler(event, context):
    for result in results["results"]["bindings"]:
        messages, images, coordinates = create_tweet(result)
        post_tweet(messages, images, coordinates)
    
        print(messages)
        print(coordinates)
        print(images)
        break

