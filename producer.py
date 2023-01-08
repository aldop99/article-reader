from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging as log
import json
import requests
import requests
from mediawiki import MediaWiki
import datetime
import time
from dotenv import load_dotenv
import os

load_dotenv()

date = datetime.datetime.today().strftime('%Y-%m-%d')


def searhMediaWiki(x):
    wikipedia = MediaWiki()
    try:
        k = wikipedia.summary(x, redirect=True)
        if (len(k) >= 1):
            return (k)
    except:
        # Decide what to do if produce request failed...
        print("does not match any pages. Try another query!")
        pass


collection = ['Elon_Musk', 'Ukraine', 'IOT', 'Smart_Home',
              'Metaverse', 'Google', 'Blockchain', 'NASA', 'source_domain_name']
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
api_call_time = 7200 #Set time in seconds.
newapi_key = os.environ.get("NEWSAPI_KEY")
while True:
    for i in range(len(collection)):
        url = f"https://newsapi.org/v2/everything?q={collection[i]}&language=en&apiKey={newapi_key}"

        response = requests.get(url)

        data = response.json()
        print(response)
        articles = data.get('articles')

        print(len(articles))
        print('%s', articles[0]['content'])
        source = articles[i]['source']
        sourceName = source['name']

        print(sourceName)
        media = searhMediaWiki(sourceName)

        user_encode_data = json.dumps(articles).encode('utf-8')

    # Asynchronous by default

        #  future = producer.send('Elon', user_encode_data )
        producer = KafkaProducer(key_serializer=str.encode)
        future1 = producer.send(
            collection[i], key=collection[i], value=user_encode_data)

        # Block for 'synchronous' sends
        try:
            record_metadata = future1.get(timeout=10)
        except KafkaError:
            # Decide what to do if produce request failed...
            log.exception()
            pass

        producer.flush()
    time.sleep(api_call_time)
