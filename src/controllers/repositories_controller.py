import numpy as np
from src.app import app
from flask import request
from src.database import db
from src.helpers.json_response import asJsonResponse
from src.students_update import pulsldata,students_to_db,labs_to_db


@app.route("/<lab>/create",endpoint='func3')
@asJsonResponse
def get_repositories(lab):
    lab_data = db["labs"].find_one({"name" : lab})
    if lab_data == None
        labs_to_db(pulsldata())
    lab_data = db["labs"].find_one({"name" : lab})
    return lab_data
    