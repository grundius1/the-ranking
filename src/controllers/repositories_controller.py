import numpy as np
from src.app import app
from flask import request
from src.database import db
from src.helpers.json_response import asJsonResponse
from src.students_update import pulsldata,labs_to_db
import src.repositories_update as repo


@app.route("/<lab>/create",endpoint='func3')
@asJsonResponse
def get_repositories(lab):
    lab_data = db["labs"].find_one({"name" : lab})
    if lab_data == None:
        labs_to_db(pulsldata())
    lab_data = db["labs"].find_one({"name" : lab})
    return lab_data
    

@app.route("/lab/update",endpoint='func4')
@asJsonResponse
def update_repositories():
    if all == True:
        repo.repo_updater(all=all)
    else:
        repo.repo_updater()
    