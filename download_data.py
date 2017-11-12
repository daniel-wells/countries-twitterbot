import requests
import json
from urllib.parse import unquote

# Search wikidata for data on countries

# Load SPARQL query
with open('query.sparql', 'r') as queryfile:
    query = queryfile.read()

# practice /test at https://query.wikidata.org
url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
results = requests.get(url, params={'query': query, 'format': 'json'}).json()

print("{} {}".format(len(results["results"]["bindings"]), "records"))

# sort countries by wikidata ID - makes diffs easier
results["results"]["bindings"].sort(key=lambda k: k['country']['value'])

# Save Data to json
with open('data.json', 'w') as outfile:
    json.dump(results, outfile, indent=4, ensure_ascii=False, sort_keys=True)

# Download and save wikimedia image
def download_image(result, type):
    filename = 'images/' + result["countryLabel"]["value"] + '_' + type + '.png'
    print(filename)
    request = requests.get(convert_url(result[type]["value"]), stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

# Convert SVG URL to PNG URL
# Don't want SVG so need to get PNG url from wikimedia API (url not predictable from svg name)
def convert_url(url):
    url = url.replace("http://commons.wikimedia.org/wiki/Special:FilePath/","")
    url = url.replace("%20","_")
    wikiimage = requests.get('https://commons.wikimedia.org/w/api.php', params={'action': 'query', 'format': 'json', 'prop': 'imageinfo','iiprop': 'url','iiurlwidth':'1000','indexpageids':'','titles': 'File:' + unquote(url)}).json()
    pageid = wikiimage['query']['pageids'][0]
    return wikiimage['query']['pages'][pageid]['imageinfo'][0]['thumburl']

# Download flag and map images
for result in results["results"]["bindings"]:
    download_image(result, "flag")
    download_image(result, "map")


# for wikipedia links add
# OPTIONAL {     ?article schema:about ?country .
#     ?article schema:isPartOf <https://en.wikipedia.org/>.
#      SERVICE wikibase:label {bd:serviceParam wikibase:language "en"}
#               }