import sys
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
from src.database import db
import re



def pulsldata(apiKey=os.getenv("API_KEY")):
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    url = "https://api.github.com/repos/ironhack-datalabs/datamad0820/pulls"
    data = []
    for i in list(range(1,5000)):
        params = {
            "page":f"{i}",
            "state":"all"
            }
        res = requests.get(url, params=params, headers=headers)
        print(f"Request data to {res.url} status_code:{res.status_code}",end="\r")
        if len(res.json()) ==0:
            break
        else:
            data.extend(res.json())
    print()
    return data
        
        
def students_to_db(studentslist):
    for item in studentslist:
        db.people.replace_one({ "gthubid": item["user"]["id"] },
            { 
            #"Name":item["title"].split("]")[1].strip(),
            "githubuser":item["user"]["login"],
            "gthubid":item["user"]["id"]
            },
            upsert=True)


def labs_to_db(studentslist):
    labs=[]
    for item in studentslist:
        title = re.sub(r"\[|\]","",item["title"].split()[0])
        labs.append(title)
    labs=set(labs)
    for item in labs:
        db.labs.replace_one({ "title": item },
            { 
            "Name":item,
            },
            upsert=True)







if __name__== "__main__":
    print(len(pulsldata()))
    labs_to_db(pulsldata())