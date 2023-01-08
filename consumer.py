from kafka import KafkaConsumer
from pymongo import MongoClient
import json
from pymongo import MongoClient
import datetime

myclient = MongoClient("mongodb://localhost:27017/")
db = myclient["news_database"]
collections = db

topics = ['Elon_Musk', 'Ukraine', 'IOT', 'Smart_Home', 'Metaverse',
          'Google', 'Blockchain', 'NASA', 'source_domain_name']

my_consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group')


for message in my_consumer:
    i = 0
    k = json.loads(message.value)

    for i in range(len(k)):
        print((k[i]))
        url = k[i]['url']
        title = k[i]['title']
        if (message.topic == 'Ukraine'):
            collections.ukraine.insert_one({
                'key': message.key,
                'title': title,
                'url': url,
                'value': k[i],
                'date': datetime.datetime.utcnow()
            })
        elif (message.topic == 'Elon_Musk'):
            try:
                collections.elon_musk.insert_one({
                    'key': message.key,
                    'title': title,
                    'url': url,
                    'value': k[i],
                    'date': datetime.datetime.utcnow()
                })
            except:

                print("Is already excist")
                pass
            collections.elon_musk.create_index('url', unique=True)
        elif (message.topic == 'IOT'):
            collections.iot_collection.insert_one({
                'key': message.key,
                'title': title,
                'url': url,
                'value': k[i],
                'date': datetime.datetime.utcnow()
            })
        elif (message.topic == 'Smart_Home'):
            collections.smart_home.insert_one({
                'key': message.key,
                'title': title,
                'url': url,
                'value': k[i],
                'date': datetime.datetime.utcnow()
            })
        elif (message.topic == 'Metaverse'):
            collections.metaverse.insert_one({
                'key': message.key,
                'title': title,
                'url': url,
                'value': k[i],
                'date': datetime.datetime.utcnow()
            })
        elif (message.topic == 'Google'):
            collections.google_collection.insert_one({
                'key': message.key,
                'title': title,
                'url': url,
                'value': k[i],
                'date': datetime.datetime.utcnow()
            })
        elif (message.topic == 'Blockchain'):
            collections.blockchain.insert_one({
                'key': message.key,
                'title': title,
                'url': url,
                'value': k[i],
                'date': datetime.datetime.utcnow()
            })
        elif (message.topic == 'NASA'):
            collections.nasa.insert_one({
                'key': message.key,
                'title': title,
                'url': url,
                'value': k[i],
                'date': datetime.datetime.utcnow()
            })
        elif (message.topic == 'source_domain_name'):
            collections.source_domain_name.insert_one({
                'key': message.key,
                'title': title,
                'url': url,
                'value': k[i],
                'date': datetime.datetime.utcnow()
            })
