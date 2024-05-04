from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from auth import login_required
import config
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
# client = MongoClient("mongodb://{}:{}@{}".format(config["username"], config["password"], config["ip_address"]))
client = MongoClient("localhost", 27017)
# if name length is odd, database1
database1 = client['washelters1']
# if name length is even, database2
database2 = client['washelters2']
databases = [database1, database2]


def hashName(name):
    db_num = len(name) % 2
    return db_num

bp = Blueprint('shelter_directory', __name__, url_prefix='/shelter_directory')

@bp.route('/', methods=('GET', 'POST'))
def shelter_directory():
    shelter_db1 = database1["shelters"]
    shelter_db2 =database2["shelters"]
    result1 = list(shelter_db1.find())
    result2 = list(shelter_db2.find())
    results = result1 + result2
    results = [x for x in results if 'city' in x.keys()]  
    results = sorted(results, key=lambda x: x["city"])
    first_letter = results[0]['city'][0]

    #directory = {first_letter: []}
    #for i in results:
    #    if (first_letter != results[i]['city'][0]):
    #        first_letter = results[i]['city'][0]
    #        directory[first_letter] = [results[i]]
    #    else:
    #        directory[first_letter].append(results[i])
    return render_template('shelter_directory.html', shelter_results=results)