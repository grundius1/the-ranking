import numpy as np
from src.app import app
from flask import request
from src.database import db
from src.helpers.json_response import asJsonResponse
from src.students_update import pulsldata,students_to_db


@app.route("/lab/create",endpoint='func3')
@asJsonResponse
def get_repositories():
    pass