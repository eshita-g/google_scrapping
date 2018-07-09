import pandas as pd
from pymongo import MongoClient                                                                #importing modules
client =MongoClient("mongodb://localhost:27017/")                                            #client connection
db =client["coaching"]
collection =db['google']
list =[]
df =collection.find()
for i in df:
    list.append(str(i))
j =pd.DataFrame(list)
j.to_csv("/home/thebrain-eshita/Documents/g2.csv")                                #writing to csv