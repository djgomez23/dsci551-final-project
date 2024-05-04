from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from auth import login_required
import config
from pymongo import MongoClient
from bson.objectid import ObjectId
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

bp = Blueprint('delete', __name__, url_prefix='/delete')

@bp.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    session_access = session.get('access')
    if (session_access == 'employee'):
        msg = 'Unauthorized operation for employees.'
        return redirect(url_for("employee.petSearch"))
    error = None
    if (request.method == 'POST'):
        form_keys = request.form.keys()
        username = None
        if ('username' in form_keys):
            username = request.form["username"]
        first_name = None
        if ('first_name' in form_keys):
            first_name = request.form["first_name"]
        last_name = None
        if ('last_name' in form_keys):
            last_name = request.form["last_name"]
        if (not username):
            error = 'Username required.'
        if (error is None):
            db_num = hashName(username)
            db = databases[db_num]
            users = db["users"]
            subject_match = users.find_one({"username": username})
            if (subject_match is None):
                error = "No user with {} username is found.".format(username)
            else:
                users.remove({"username": username})
        if (error is None):
            flash('Success!', category='message')
            return redirect(url_for("dbm_query.dbm_query"))
    flash(error, category='error')
    return render_template(
        'guis/delete/user.html',
        query_options=[
            {"option": ["first_name", "First Name"]},
            {"option": ["last_name", "Last Name"]},
            {"option": ["username", "Username"]}
        ]
    )

@bp.route('/pet', methods=['GET', 'POST'])
@login_required
def pet():
    session_access = session.get('access')
    if (session_access == 'employee'):
        msg = 'Unauthorized operation for employees.'
        return redirect(url_for("employee.petSearch"))
    error = None
    if (request.method == 'POST'):
        form_keys = request.form.keys()
        pet_name = None
        if ('pet_name' in form_keys):
            pet_name = request.form['pet_name']
        microchip = None
        if ('microchip' in form_keys):
            microchip = request.form['microchip']
        gender = None
        if ('gender' in form_keys):
            gender = request.form['gender'].lower()
        pet_type = None
        if ('pet_type' in form_keys):
            pet_type = request.form['pet_type'].lower()
        if (not microchip):
            error = 'Microchip required.'
        print(error)
        if (error is None):
            db_num = hashName(pet_name)
            db = databases[db_num]
            pets = db["pets"]
            subject_match = pets.find_one({"microchip": int(microchip)})
            if (subject_match is None):
                error = "No pet with {} microchip is found.".format(microchip)
            else:
                pets.remove({"microchip": int(microchip)})
            print(error)
        if (error is None):
            flash('Success!', category='message')
            return redirect(url_for("dbm_query.dbm_query"))
    flash(error, category='error')
    return render_template(
        'guis/delete/pet.html',
        query_options=[
            {"option": ["pet_name", "Pet Name"]},
            {"option": ["microchip", "Microchip Number"]},
            {"option": ["gender", "Gender"]},
            {"option": ["pet_type", "Pet Type"]}
        ]
    )

@bp.route('/shelter', methods=['GET', 'POST'])
@login_required
def shelter():
    session_access = session.get('access')
    if (session_access == 'employee'):
        msg = 'Unauthorized operation for employees.'
        return redirect(url_for("employee.petSearch"))
    error = None
    if (request.method == 'POST'):
        form_keys = request.form.keys()
        shelter_name = None
        if ('shelter_name' in form_keys):
            shelter_name = request.form["shelter_name"]
        city = None
        if ('city' in form_keys):
            city = request.form["city"]
        if (not shelter_name):
            error = 'Shelter name required.'
        elif (not city):
            error = 'City required'
        if (error is None):
            db_num = hashName(shelter_name)
            db = databases[db_num]
            shelters = db["shelters"]
            find_query = {}
            find_query['name'] = shelter_name
            if ((city != '') and (city is not None)):
                find_query['city'] = city
            subject_match = shelters.find_one(find_query)
            if (subject_match is None):
                error = "No shelter with the name {} is found.".format(shelter_name)
            else:
                shelters.remove({"name": shelter_name})
        if (error is None):
            flash('Success!', category='message')
            return redirect(url_for("dbm_query.dbm_query"))
    flash(error, category='error')
    return render_template(
        'guis/delete/shelter.html',
        query_options=[
            {"option": ["shelter_name", "Shelter Name"]},
            {"option": ["city", "City"]}
        ]
    )