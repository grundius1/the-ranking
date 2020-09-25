import sys
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
import re
from src.database import db
from src.students_update import pulsldata,labs_to_db
from datetime import timedelta,datetime


def get_total_gitrepos(apiKey=os.getenv("API_KEY")):
    '''
    gives the last pull request in datamad0820
    '''
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    url1 = "https://api.github.com/repos/ironhack-datalabs/datamad0820/pulls?page=1&per_page=1&state=all"
    res = requests.get(url1, headers=headers)
    repos = res.json()
    return repos[0]["number"]

def get_total_dbrepos(all = False):
    '''
    create a list for the repos to update
    '''
    data = db["repositories"].find({"state":"closed"})
    repos = get_total_gitrepos()
    totalrepos = list(range(1,repos+1))
    if all == False:
        for item in list(data):
            totalrepos.remove(item["number"])
        return totalrepos
    else:
        return totalrepos

def repo_updater(all ,apiKey=os.getenv("API_KEY") ):
    '''
    creates a list wuith the info of all the pull requests
    '''
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    repolist =[]
    max_repos = get_total_dbrepos(all)
    for item in max_repos:
        url = f"https://api.github.com/repos/ironhack-datalabs/datamad0820/pulls/{item}"
        res = requests.get(url, headers=headers)
        print(f"getting repo Nº{item}")
        if res.status_code == 404:
            pass
        else:
            repolist.append(res.json())
    return repolist

def repo_to_db(repolist):
    '''
    loads all the pulls into the database
    '''
    labs_to_db(pulsldata())
    previous_lab_name = ''
    for item in repolist:
        commentsurl = item["comments_url"]
        comments = commentsgetter(commentsurl)
        memes = meme_identifier(comments)
        puller = db.people.find_one({ "gthubid" : item["user"]["id"]},{"_id":1}).values()
        collaborators = collaborators_identifier(comments)
        collaborators.extend(puller)
        title = previous_lab_name if len(re.findall(r"\[lab-.+\]",item["title"]))==0 else re.findall(r"\[lab-.+\]",item["title"])
        previous_lab_name = title
        labname = db["labs"].find_one({"Name": title[0]})["_id"]
        last_commit = item["commits_url"]
        last_commit = commentsgetter(last_commit)
        last_commit = last_commit[-1]["commit"]["committer"]["date"]
        initdic= {
            "number" : item["number"],
            "state" : item["state"],
            "title" : labname,
            "collaborators": collaborators
        }
        print(f"inserting commit {item['number']}")
        if item["state"] == "closed":               
                initdic.update({
                        "memes": memes,
                        "correction_time" : str(timegetter(item["closed_at"])-timegetter(last_commit)),
                        })
                db.repositories.replace_one({ "number": item["number"]},
                   initdic,
                   upsert=True)                
        else:
            db.repositories.replace_one({ "number": item["number"]},
                initdic,
                upsert=True)
    
def timegetter(strtime):
    '''
    transform datetime string to datetime item
    '''
    date_format = "%Y-%m-%dT%H:%M:%S" 
    time = datetime.strptime(strtime[:19], date_format)
    return time


def commentsgetter(url, apiKey=os.getenv("API_KEY")):
    '''
    given an url it makes a call to the url and return the data in JSON
    '''
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    return data

def meme_identifier(data):
    '''
    identifies an image in the comments of the pull
    '''
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

def collaborators_identifier(data):
    '''
    identifies all the students who have made comments in a pull
    '''
    collaborators = []
    teachers_id = [52798316,52798316,49686519,57899051]
    for item in range(len(data)):
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
