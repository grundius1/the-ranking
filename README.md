# the-ranking

## Purpose
this application collects data from Github datamad 0820 repository and save it in a mongodb database, and allows you to consult and update the mongo db database

## libraries

sys
numpy
os
dotenv
flask
json
requests
datetime
random
pymongo

## Usage

	-'/' endpoint : welcome to the api 
	-'/student/all': allows yo to view all students in the database
	-'/create/<studentname>' : allows you to search a student in the database, if the student is not present it will update the students collection and search again
	-'/<lab>/create': allows you to search a lab in the database aans update all the database if the -lab is not in the collection
	-'/lab/update' : this call updates the repositories collection, if parameter all=True given, it will update all the repositories, in False or not given it will only update the openes and new pulls in github
	-'/<lab_id>/search': allows you to search data of specific labs if parameter name given it gives info about a lab and specific student
	-'/lab/<lab_id>/meme' : gives a random meme from the ones used in all comments
	-'/lab/memeranking' : gives a ranking of the most used memes and the labs where it belongs



