from kafka import KafkaConsumer
from pymongo import MongoClient
import datetime
import json

consumer = KafkaConsumer('my-topic', bootstrap_servers='localhost:9092')

client = MongoClient('mongodb://localhost:27017/')
db = client['news_database']
collection = db

topics = ['Elon_Musk', 'Ukraine', 'IOT', 'Smart_Home', 'Metaverse', 'Google', 'Blockchain', 'NASA']

consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group')

for message in consumer:
    i = 0
    k = json.loads(message.value)    
    no = len(k)

    articles_added = 0
    articles_not_added = 0

    for i in range(len(k)):
        # print((k[i]))
        url = k[i]['url']
        title = k[i]['title']

        if (message.topic == 'Ukraine'):
            try:
                collection.ukraine.insert_one({
                    'key': message.key,
                    'title': title,
                    'url': url,
                    'value': k[i],
                    'date': datetime.datetime.utcnow()
                })
            except:                
                print("Is already exist")
                pass
            collection.ukraine.create_index('url', unique=True)
        elif (message.topic == 'Elon_Musk'):
            try:
                collection.elon_musk.insert_one({
                    'key': message.key,
                    'title': title,
                    'url': url,
                    'value': k[i],
                    'date': datetime.datetime.utcnow()
                })
            except:
                print("Is already exist")
                pass
            collection.elon_musk.create_index('url', unique=True)
        elif (message.topic == 'IOT'):
            try:
                collection.iot.insert_one({
                    'key': message.key,
                    'title': title,
                    'url': url,
                    'value': k[i],
                    'date': datetime.datetime.utcnow()
                })
                print('\n'+title)
            except:
                print("\nIs already exist")
                pass
            collection.iot.create_index('url', unique=True)                
        elif (message.topic == 'Smart_Home'):
            try:
                collection.smart_home.insert_one({
                    'key': message.key,
                    'title': title,
                    'url': url,
                    'value': k[i],
                    'date': datetime.datetime.utcnow()
                })
            except:
                print("Is already exist")
                pass
            collection.smart_home.create_index('url', unique=True)                        
        elif (message.topic == 'Metaverse'):
            try:
                collection.metaverse.insert_one({
                    'key': message.key,
                    'title': title,
                    'url': url,
                    'value': k[i],
                    'date': datetime.datetime.utcnow()
                })
            except:
                print("Is already exist")
                pass
            collection.metaverse.create_index('url', unique=True)
        elif (message.topic == 'Google'):
            try:
                collection.google.insert_one({
                    'key': message.key,
                    'title': title,
                    'url': url,
                    'value': k[i],
                    'date': datetime.datetime.utcnow()
                })
            except:
                print("Is already exist")
                pass
            collection.google.create_index('url', unique=True)
        elif (message.topic == 'Blockchain'):
            try:
                collection.blockchain.insert_one({
                    'key': message.key,
                    'title': title,
                    'url': url,
                    'value': k[i],
                    'date': datetime.datetime.utcnow()
                })
            except:
                print("Is already exist")
                pass
            collection.blockchain.create_index('url', unique=True)    
        elif (message.topic == 'NASA'):
            try:
                collection.nasa.insert_one({
                    'key': message.key,
                    'title': title,
                    'url': url,
                    'value': k[i],
                    'date': datetime.datetime.utcnow()
                })
            except:
                print("Is already exist")
                pass
            collection.nasa.create_index('url', unique=True)
print("Success")   