from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import pymongo

# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["n_db"]

# Find all collections in the database
collections = db.list_collection_names()

# Initialize a dictionary to store collection names and their corresponding counts
dates_results = {}
articles_results = {}

a = []
get_topics = []

# Loop through all collections
for collection_name in collections:
    # Skip processing the "users" collection
    if collection_name == "users":
        continue

    # Access the collection
    collection = db[collection_name]
    
    # Find all documents in the collection and create a list of the "publishedAt" field
    published_at_values = [document["value"]["publishedAt"] for document in collection.find()]

    # Use Counter to count the occurrences of each unique "publishedAt" value
    counts = Counter(published_at_values)

    # Initialize a list to store the count values for this collection
    dates_list = []
    counts_list = []

    date_from = datetime.strptime("30 January 2023", "%d %B %Y").date()
    date_to = datetime.strptime("25 January 2023", "%d %B %Y").date()

    date_from_str = date_from.strftime("%d %B %Y")
    date_to_str = date_to.strftime("%d %B %Y")

    for value, count in counts.items():
        if value <= date_from_str and value > date_to_str:
            dates_list.append(value)
            counts_list.append(count)
    
    # Add the results for this collection to the dictionary
    dates_results[collection_name] = dates_list
    articles_results[collection_name] = counts_list

    get_topics.append(collection_name)
    topics = [s.replace('_', ' ').title() for s in get_topics]

    # sort it
    plot_dates = [value for value, count in counts.items()
        if value <= date_from_str and value > date_to_str]

    y = [count for value, count in counts.items()
        if value <= date_from_str and value > date_to_str]
    
    plot_dates, y = zip(*sorted(zip(plot_dates, y)))

    xl = list(plot_dates)
    yl = list(y)

    a.append(yl)

res = []
for i, lst in enumerate(a):
    while len(lst) < 5:
        lst.append(0)
    res.append(lst)    

list1, list2, list3, list4, list5, list6, list7, list8 = [res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7]]

plot_dates = []

# Insert dates to the list
for i in range((date_from - date_to).days):
    date = (date_to + timedelta(days=i)).strftime("%d %B %Y")
    plot_dates.append(date)

y1 = np.array(list1)
y2 = np.array(list2)
y3 = np.array(list3)
y4 = np.array(list4)
y5 = np.array(list5)
y6 = np.array(list6)
y7 = np.array(list7)
y8 = np.array(list8)

# Set the figure size
plt.figure(figsize=(10, 6))

# plot bars in stack manner
plt.bar(plot_dates, y1, color='red')
plt.bar(plot_dates, y2, bottom=y1, color='green')
plt.bar(plot_dates, y3, bottom=y1+y2, color='blue')
plt.bar(plot_dates, y4, bottom=y1+y2+y3, color='yellow')
plt.bar(plot_dates, y5, bottom=y1+y2+y3+y4, color='purple')
plt.bar(plot_dates, y6, bottom=y1+y2+y3+y4+y5, color='orange')
plt.bar(plot_dates, y7, bottom=y1+y2+y3+y4+y5+y6, color='grey')
plt.bar(plot_dates, y8, bottom=y1+y2+y3+y4+y5+y6+y7, color='black')

plt.xlabel("Days")
plt.ylabel("No of Articles")
plt.legend(topics)
plt.title(f"Articles of each topic posted from {date_from_str} to {date_to_str}")
plt.savefig("mygraph.png")
plt.show()