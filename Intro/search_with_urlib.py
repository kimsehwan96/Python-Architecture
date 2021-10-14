import json
from urllib.request import urlopen
from urllib.parse import urlencode

params = dict(
    q='Hello',
    format='json'
)

handler = urlopen(
    'http://api.duckduckgo.com' + '?' + urlencode(params)
)

raw_text = handler.read().decode('utf8')
parsed = json.loads(raw_text)

results = parsed[
    'RelatedTopics'
]

for result in results:
    if 'Text' in result:
        print(result['FirstURL'] + ' - ' + result['Text'])

