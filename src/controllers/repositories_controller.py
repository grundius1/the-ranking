import numpy as np
from src.app import app
from flask import request
from src.database import db
from src.helpers.json_response import asJsonResponse
from src.students_update import pulsldata,labs_to_db
import src.repositories_update as repo
import random


@app.route("/<lab>/create")
@asJsonResponse
def get_repositories(lab):
    lab_data = db["labs"].find_one({"Name" : lab})
    if lab_data == None:
        labs_to_db(pulsldata())
    lab_data = db["labs"].find_one({"Name" : lab},{"_id" : 1})
    return lab_data["_id"]
    

@app.route("/lab/update")
@asJsonResponse
def update_repositories():
    all = request.args.get("all")
    if all == "True":
        repo.repo_to_db(repo.repo_updater(True))
    else:
        repo.repo_to_db(repo.repo_updater(False))
    return "repositories status updated in db"
    
@app.route("/<lab_id>/search")
@asJsonResponse
def get_student_sub(lab_id):
    lab = "["+lab_id+"]"
    lab = db["labs"].find_one({"Name": lab})
    name = request.args.get("name")
    if name:
        name = db["people"].find_one({"githubuser": name})
        response = db["repositories"].find({"$and" :[{"collaborators": name["_id"]} , {"title" : lab["_id"]}]})
        response = list(response)
        for item in response:
            item["title"] = db["labs"].find_one({"_id": item["title"]},{"_id":0})
            for index, person in enumerate(item["collaborators"]):
                item["collaborators"][index] = db["people"].find_one({"_id": person},{"_id":0})
        return response
    else:
        response = db["repositories"].find({"title" : lab["_id"]})
        response = list(response)
        total_pulls = len(response)
        closed = 0
        for item in response:
            if item["state"]== "closed":
                closed += 1
        opened = total_pulls - closed
        percentage = (closed/total_pulls)*100
        students = db["people"].find()
        students=list(students)
        students_out = set()
        for item in students:
            puller = item["_id"]
            for pull in response:
                if puller not in pull["collaborators"]:
                    students_out.add(item["githubuser"])
                else:
                    try:
                        students_out.remove(item["githubuser"])
                        break
                    except:
                        break
        memes = set()
        correction_time =[]
        for item in response:
            for meme in item["memes"]:
                memes.add(meme)
            correction_time.append(item["correction_time"])
        return [{
            "open_pr": opened,
            "closed_pr" : closed,
            "percentage" : percentage,
            "missing_students": list(students_out),
            "memes": list(memes),

        }]

        


@app.route("/lab/<lab_id>/meme")
@asJsonResponse
def get_meme(lab_id):
    lab = "["+lab_id+"]"
    lab = db["labs"].find_one({"Name": lab})["_id"]
    repos = db["repositories"].find({"$and" :[{"state": "closed"} , {"title" : lab}]})
    memes = []
    for item in list(repos):
        memes.extend(item["memes"])
    print(memes)
    return random.choice(memes)

@app.route("/lab/memeranking")
@asJsonResponse
def get_memeranking():
    memes = db.repositories.aggregate([
        {"$unwind": "$memes" },
        {'$group': {'_id': {"state":"$state", "meme":"$memes", "title": "$title"},'count': {'$sum': 1}}}
    ])#.sort({"_id.count":1})
    memes_clean=[]

    #print(len(list(memes)[0]))
    for item in list(memes):
        dic = item["_id"]
        item.pop("_id")
        dic.update(item)
        memes_clean.append(dic)
    
    for item in memes_clean:
        item["title"] = db["labs"].find_one({"_id": item["title"]})["Name"]
    print(memes_clean)
    #    memes_clean.append(item["_id"])
        #["title"] = db["labs"].find_one({"_id": item["_id"]["title"]},{"_id":0})
    memes_clean = sorted(memes_clean, key = lambda x: x["count"], reverse=True)
    return memes_clean
    