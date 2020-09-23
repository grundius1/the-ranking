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

def get_total_dbrepos(all = False):
    data = db["repositories"].find()
    repos = get_total_gitrepos()
    totalrepos = list(range(1,repos+1))
    if all == False:
        for item in list(data):
            totalrepos.remove(item["number"])
    else:
        return totalrepos
    

def repo_updater(apiKey=os.getenv("API_KEY")):
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    repolist =[]
    max_repos = get_total_dbrepos()
    for item in max_repos:
        url = f"https://api.github.com/repos/ironhack-datalabs/datamad0820/pulls/{item}"
        res = requests.get(url, headers=headers)
        if res.status_code == 404:
            pass
        else:
            repolist.append(res.json())
    return repolist

def repo_to_db(repolist):
    for item in repolist:
        commentsurl = item["comments_url"]
        comments = commentsgetter(commentsurl)
        memes = meme_identifier(comments)
        puller = db.people.find_one({ "gthubid" : item["user"]["id"]},{"_id":1}).values()
        collaborators = collaborators_identifier(comments)
        collaborators.extend(puller)
        #print(item["number"])
        #print(item["title"].split()[0].replace("[","").replace("]",""))
        #print(item["state"])
        initdic= {
            "number" : item["number"],
            "state" : item["state"],
            "title" : item["title"].split()[0].replace("[","").replace("]",""),
            "created_date" : item["created_at"]
        }
        for value in range(len(collaborators)):
            initdic.update({
                f"collaborator {value+1}": collaborators[value]
            })

        if item["state"] == "closed":
            if len(memes) != 0:
                for meme in range(len(memes)):
                    initdic.update({
                        f"meme {meme+1}": memes[meme]
                        })
                db.repositories.replace_one({ "number": item["number"]},
                   initdic,
                   upsert=True)
            else:
                db.repositories.replace_one({ "number": item["number"]},
                   initdic,
                   upsert=True)
                
        else:
            db.repositories.replace_one({ "number": item["number"]},
                initdic,
                upsert=True)


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
        memes = re.findall(regex,item["body"])
        for meme in range(len(memes)):
            if len(memes[meme]) == 0:
                pass
            else:
                urlclean= re.sub(r"\(|\)","",memes[meme])
                memesurl.append(urlclean)
    if len(memesurl) == 0:
        return []
    else:
        return memesurl



    #googleurl = "https://images.google.com/searchbyimage?image_url="
    #for item in memesurl:
    #    print(item)
    #    response = requests.get(googleurl+item)
    #    soup = BeautifulSoup(response.text, 'html.parser')
    #    print(soup.find_all("input", maxlength="2048"))


def collaborators_identifier(data):
    #print(data)
    collaborators = []
    teachers_id = [52798316,52798316,49686519,57899051]
    for item in range(len(data)):
        #print(type(item))
        if data[item]["user"]["id"] in teachers_id:
            pass
        else:
            collaborator = db.people.find_one({ "gthubid" : data[item]["user"]["id"]},{"_id":1})
            collaborators.append(collaborator["_id"])
    if len(collaborators) == 0:
        return []
    else:
        return collaborators




if __name__== "__main__":
    #meme_identifier()
    #collaborators_identifier(commentsgetter("https://api.github.com/repos/ironhack-datalabs/datamad0820/issues/2/comments"))
    repo_to_db(repo_updater())
    #get_total_dbrepos()
