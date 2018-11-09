import json
import os
import pymongo
import getpass

def main():
    f = []
    for (dirpath, dirnames, filenames) in os.walk('./player_jsons'):
        f.extend([os.path.join(dirpath, filename) for filename in filenames])

    username = input("Username: ")
    pswd = getpass.getpass('Password:')
    client = pymongo.MongoClient("mongodb+srv://"+username+":"+pswd+"@nsp-cluster-zqniz.mongodb.net/test?retryWrites=true")
    collection = client["Players"]["Players"]
    requests = []
    for filename in f:
        with open(filename) as f:
            data = json.load(f)
            requests.append(pymongo.InsertOne(data))

    try:
        collection.bulk_write(requests, ordered=False)
    except pymongo.BulkWriteError as e:
        print(e.details)

    

if __name__ == '__main__':
    main()