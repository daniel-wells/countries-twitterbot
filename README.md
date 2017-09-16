# Random Country Twitter Bot
This is a Twitter bot which posts flags and maps of random countries along with population and capital city facts.
[@randomcountries](https://www.twitter.com/randomcountries)

The bot is built on the python library [Tweepy](http://www.tweepy.org). The data is from [Wikidata](https://www.wikidata.org) accesses via their SPARQL query service, and the images of flags and maps are from [Wikimedia Commons](https://commons.wikimedia.org) using the MediaWiki API. AWS Lambda is used to host the bot which is scheduled to run every 1301 minutes resulting in 404 tweets per year (~2 per country).

To create the package for AWS lambda the Tweepy library dependency is installed in the project directory so it can be uploaded with the rest of the code
```bash
pip install tweepy -t .
```

To fit in the 50MB AWS lambda limit the images are compressed with OptiPNG. The whole directory is then zipped before uploading.