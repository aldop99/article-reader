# Retrieval, Storage & Processing Mechanism by Distributed Resources Team 10

First deliverable 
## Installation

Run with pip
```bash
pip install -r requirements.txt
```

Create a .env file in the files directory and paste your [News API](https://choosealicense.com/licenses/mit/) key
```
NEWSAPI_KEY=YOUR NEWS API KEY
```

## Usage

1. Start Zookeeper server:
```
./bin/zookeeper-server-start.sh config/zookeeper.properties
```

2. Start Kafka server:
```
./bin/kafka-server-start.sh config/server.properties
```

3. Run 
```producer.py``` 
and 
```consumer.py```