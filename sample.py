from elasticsearch import Elasticsearch
from pymongo import  MongoClient
import time
import numpy as np

conn = MongoClient("mongodb+srv://arpit:groupten123!@agnesdatabase-1mhnx.mongodb.net/Agnes?retryWrites=true")
db = conn.Agnes
usersdb = db['users']
usermodelsdb = db['usermodels']
groupsdb = db['groups']

client = Elasticsearch(host='search-agnes-mxh2gzjm4nw6frw5gweoexioqi.us-east-1.es.amazonaws.com', port=80)


def elastic_search(user_model):
    data = client.search(index="groupss", body={ "query": {


                                                "function_score": {
                                                    "score_mode": "max",
                                                    "query": {"match": {"community":"gwu"}},
                                                      "script_score": {
                                                        "script": {
                                                              "lang": "painless",
                                                            "params": {
                                                              "usermodel": user_model
                                                            },
                                                            #doc['model'][i]
                                                            #params.usermodel[i]
                                                          "inline": "float total = 0; for (int i = 0; i <1 ; ++i) { total += 1*doc['model'][i]; } return doc['model'][0];"
                                                        #,"source":"total"
                                                        }
                                                      }
                                                    }
                                                    }
                                                })
    return data

def general_search(user_model,grp_number):
    groups =groupsdb.find({'community':"gwu"})
    s = 0
    counter = 0
    all_sims = []
    for group in groups:
        counter +=1
        if counter>grp_number:
            break
        sim = np.dot(user_model, group['model'])
        all_sims.append(sim)
        s +=sim

    all_sims.sort(reverse=True)
    print(all_sims[0:5])
    return sim


def test(number_users,grp_number):

    users = usermodelsdb.find()
    whole_time_ES = 0
    whole_time_GS = 0
    couner= 0
    for user in users:
        print(user['model'])
        couner +=1
        if couner>number_users:
            break

        user_model = user['model']

        t1 = time.time()

        res = elastic_search(user_model)

        for hit in res['hits']['hits']:
            print (hit)

        t2 = time.time()

        whole_time_ES +=(t2-t1)

        t1 = time.time()

        #general_search(user_model,grp_number)

        t2 = time.time()

        whole_time_GS += (t2 - t1)

    print("ES:"+str(whole_time_ES))
    print("GS:"+str(whole_time_GS))

test(1,1000)


