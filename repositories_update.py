import sys
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
import re
from src.database import db
from src.students_update import pulsldata



def get_total_gitrepos(apiKey=os.getenv("API_KEY")):
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    url1 = "https://api.github.com/repos/ironhack-datalabs/datamad0820/pulls?page=1&per_page=1&state=all"
    res = requests.get(url1, headers=headers)
    repos = res.json()
    return repos[0]["number"]

def get_total_dbrepos():
    data = db["repositories"].find()
    if len(list(data)) == 0:
        return 0
    

def repo_updater(apiKey=os.getenv("API_KEY")):
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    repolist =[]
    max_repos = get_total_gitrepos()
    for item in range(1,5):
        url = f"https://api.github.com/repos/ironhack-datalabs/datamad0820/pulls/{item}"
        res = requests.get(url, headers=headers)
        #print(res.json())
        repolist.append(res.json())
    return repolist

def repo_to_db(repolist):
    for item in repolist:
        commentsurl = item["comments_url"]
        comments = commentsgetter(commentsurl)
        memes = meme_identifier(comments)
        collaborators = collaborators_identifier(comments)
        print(item["number"])
        print(item["title"].split()[0].replace("[","").replace("]",""))
        initdic= {
            "number" : item["number"],
            "state" : item["state"],
            "title" : item["title"].split()[0].replace("[","").replace("]","")
            "created_at" : item["created_at"],
        }
        if item["state"] == "closed":
            pass
            #db.repositories.update_one({ "number": item["number"]},
            #   "id" : item["id"],
            #   "number" : item["number"],
            #   "state" : item["state"],
            #   "title" : item["title"].split()[0].replace("[","").replace("]","")
            #   "created_at" : item["created_at"],
            #   "closed_at" : item["closed_at"],
            #   "correction_time" : item["closed_at"]-item["created_at"],
            #    "memes" : meme_identifier(item["comments_url"])
            # )
        else:
            pass
            #db.repositories.update_one({ "number": item["number"]},
            #   "id" : item["id"],
            #   "number" : item["number"],
            #   "state" : item["state"],
            #   "title" : item["title"].split()[0].replace("[","").replace("]","")
            #   "created_at" : item["created_at"]
            # )


def commentsgetter(url, apiKey=os.getenv("API_KEY")):
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    return data

def meme_identifier(data):
    #print(re.sub(r"\(|\)","",data[0]["body"]))
    regex = r"\(https://user-images.githubuser.+\)"
    memesurl=[]
    for item in data:
        #print(item)
        memesurl.extend(re.findall(regex,item["body"]))
    #print(memesurl)
    for item in range(len(memesurl)):
        if len(memesurl[item])== 0:
            pass
        else:
            urlclean= re.sub(r"\(|\)","",memesurl[item])
            memesurl[item] = urlclean
    memesdic = {}
    for item in range(len(memesurl)):
        memesdic.update({f"meme{item+1}": memesurl[item]})
    #print(memesdic)
    return memesdic



    #googleurl = "https://images.google.com/searchbyimage?image_url="
    #for item in memesurl:
    #    print(item)
    #    response = requests.get(googleurl+item)
    #    soup = BeautifulSoup(response.text, 'html.parser')
    #    print(soup.find_all("input", maxlength="2048"))


def collaborators_identifier(data):

    collaborators = []
    teachers_id = [52798316,52798316,49686519]
    for item in range(len(data)):
        if data[item]["user"]["id"] in teachers_id:
            pass
        else:
            print(data[item]["user"]["id"])
            collaborator = db.people.find_one({ "gthubid" : data[item]["user"]["id"]},{"_id":1})
            collaborators.append(collaborator)
    print(collaborators)
    return collaborators




if __name__== "__main__":
    #meme_identifier()
    collaborators_identifier()
    #repo_to_db(repo_updater())