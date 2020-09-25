import numpy as np
from src.app import app
from flask import request
from src.database import db
from src.helpers.json_response import asJsonResponse
from src.students_update import pulsldata,students_to_db


@app.route('/')
def welcome():
    return {
        "status": "OK",
        "message": "welcome to Ironhack datamad0820guithub API"
    }




@app.route("/student/all")
@asJsonResponse
def get_all_students():
    '''
    retunr all the students in the database
    '''
    data = db["people"].find()
    return data


# http://localhost:3000/saludo?color=rojo&idioma=en
@app.route("/create/<studentname>")
@asJsonResponse
def get_students(studentname):
    '''
    search for student in the database and update it if not found
    '''
    student_data = db["people"].find_one({"githubuser" : studentname})
    if student_data == None:
        students_to_db(pulsldata())
        student_data = db["people"].find_one({"githubuser" : studentname})
        if student_data == None:
            return {
            "status": "not found",
            "message": f"No ironhacker found with name {studentname} in database"
        }, 404
    return student_data
