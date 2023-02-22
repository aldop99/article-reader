import json
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging as log
import requests
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

producer = KafkaProducer(bootstrap_servers='localhost:9092')

collection = ['Elon_Musk', 'Ukraine', 'IOT', 'Smart_Home',
              'Metaverse', 'Google', 'Blockchain', 'NASA']

api_call_time = 7200 #Set time in seconds.
newapi_key = os.environ.get("NEWSAPI_KEY")
while True:
    for i in range(len(collection)):
        url = f"https://newsapi.org/v2/everything?q={collection[i]}&language=en&apiKey={newapi_key}"
        response = requests.get(url)

        data = response.json()

        # changes date format
        for article in data['articles']:
            published_at = article['publishedAt']
            published_at = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
            article['publishedAt'] = published_at.strftime("%d %B %Y")

        articles = data.get('articles')
        
        print(response)
        print(len(articles))

        user_encode_data = json.dumps(articles).encode('utf-8')
        # print(user_encode_data)

        producer = KafkaProducer(key_serializer=str.encode)
        future1 = producer.send(collection[i], key=collection[i], value=user_encode_data)        

        # Block for 'synchronous' sends
        try:
            record_metadata = future1.get(timeout=10)
        except KafkaError:
            # Decide what to do if produce request failed...
            log.exception()
            pass

        producer.flush()
    time.sleep(api_call_time)