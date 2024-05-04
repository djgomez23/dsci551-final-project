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

bp = Blueprint('update', __name__, url_prefix='/update')

@bp.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    error = None
    session_access = session.get('access')
    if (session_access == 'employee'):
        msg = 'Unauthorized operation for employees.'
        return redirect(url_for("employee.petSearch"))
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
        shelter_name = None
        if ('shelter_name' in form_keys):
            shelter_name = request.form["shelter_name"]
        new_password = None
        if ('new_password' in form_keys):
            new_password = request.form['new_password']
        access_class = None
        if ('access_class' in form_keys):
            access_class = request.form['access_class'].lower()
        
        if (not username):
            error = 'Username required.'
        if (error is None):
            db_num = hashName(username)
            db = databases[db_num]
            users = db["users"]
            subject_match = users.find_one({"username": username})
            if (subject_match is None):
                error = 'User {} does not exist.'.format(username)
            else:
                hashed_pass = None
                if (new_password is not None):
                    hashed_pass = generate_password_hash(new_password)
                shelter_id = None
                if ((shelter_name is not None) and (shelter_name != '')):
                    shelter_db_num = hashName(shelter_name)
                    shelter_db = databases[shelter_db_num]
                    shelter = shelter_db["shelters"].find_one({"name": shelter_name})
                    # check to see if the shelter exists
                    
                    if (shelter is None):
                        error = "Please enter a valid shelter name or add a new shelter to the database."
                    else:
                        shelter_id = shelter["_id"]
                attributes = {
                    "password": hashed_pass,
                    "access_class": access_class,
                    "first_name": first_name,
                    "last_name": last_name,
                    "shelter_id": shelter_id
                }
                filtered_attributes = {key: value for key, value in attributes.items() if ((value != '') and (value is not None))}
                users.update_one({"username": username}, {"$set": filtered_attributes})
            print(error)
            if (error is None):
                flash('Success!', category='message')
                return redirect(url_for("dbm_query.dbm_query"))
    flash(error, category='error')
    return render_template(
        'guis/update/user.html',
        query_options=[
            {"option": ["username", "Username"]},
            {"option": ["first_name", "First Name"]},
            {"option": ["last_name", "Last Name"]},
            {"option": ["new_password", "New Password"]},
            {"option": ["access_class", "Access Class"]},
            {"option": ["shelter_name", "Shelter Name"]}
        ]
    )

@bp.route('/pet', methods=['GET', 'POST'])
@login_required
def pet():
    error = None
    session_access = session.get('access')
    if (session_access == 'employee'):
        msg = 'Unauthorized operation for employees.'
        return redirect(url_for("employee.petSearch"))
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
        fixed = None
        if ('fixed' in form_keys):
            fixed = request.form['fixed']
        adopted = None
        if ('adopted' in form_keys):
            adopted = request.form['adopted']
        adoption_date = None
        if ('adoption_date' in form_keys):
            adoption_date = request.form['adoption_date']
        shelter_name = None
        if ('shelter_name' in form_keys):
            shelter_name = request.form['shelter_name']
        birthday = None
        if ('birthday' in form_keys):
            birthday = request.form['birthday']
        breed = None
        if ('breed' in form_keys):
            breed = request.form['breed'].lower()
        colors = None
        if ('colors' in form_keys):
            colors = request.form['colors'].lower()
        medical_record = None
        if ('medical_record' in form_keys):
            medical_record = request.form['medical_record']
        home_preference = None
        if ('home_preference' in form_keys):
            home_preference = request.form['home_preference'].lower()
        temperament = None
        if ('temperament' in form_keys):
            temperament = request.form['temperament'].lower()
        previously_adopted = None
        if ('previously_adopted' in form_keys):
            previously_adopted = request.form['previously_adopted']
        reason_for_admittance = None
        if ('reason_for_admittance' in form_keys):
            reason_for_admittance = request.form['reason_for_admittance']
        
        if (not pet_name):
            error = 'Username required.'
        elif (not microchip):
            error = 'Please enter a valid microship number.'
        elif (not gender):
            error = 'Please enter the gender of the pet.'
        elif (not pet_type):
            error = 'Please indicate the type of pet'
        if (error is None):
            db_num = hashName(pet_name)
            db = databases[db_num]
            pets = db["users"]
            subject_match = pets.find_one({"microchip": int(microchip)})
            if (subject_match is None):
                error = 'Pet with {} microchip does not exist.'.format(microchip)
            else:
                if (fixed == 'True'):
                        fixed = True
                elif (fixed == 'False'):
                        fixed = False
                if (adopted == 'True'):
                        adopted = True
                elif (adopted == 'False'):
                        adopted = False
                if (previously_adopted == 'True'):
                        previously_adopted = True
                elif (previously_adopted == 'False'):
                        previously_adopted = False
                attributes = {
                    "fixed": fixed,
                    "adopted": adopted,
                    "adoption_date": adoption_date,
                    "birthday": birthday,
                    "colors": colors,
                    "breed": breed,
                    "medical_record": medical_record,
                    "home_preference": home_preference,
                    "temperament": temperament,
                    "previously_adopted": previously_adopted,
                    "reason_for_admittance": reason_for_admittance
                }
                if (shelter_name):
                    shelter_db_num = hashName(shelter_name)
                    shelter_db = databases[shelter_db_num]
                    shelter = shelter_db["shelters"].find_one({"name": shelter_name})
                    # check to see if the shelter exists
                    if (shelter is None):
                        error = "Please enter a valid shelter name or add a new shelter to the database."
                    else:
                        attributes["shelter_id"] = shelter["_id"]
                print(error)
                if (error is None):
                    filtered_attributes = {key: value for key, value in attributes.items() if ((value != '') and (value is not None))}
                    pets.update_one({"microchip": microchip}, {"$set": filtered_attributes})
            if (error is None):
                flash('Success!', category='message')
                return redirect(url_for("dbm_query.dbm_query"))
    flash(error, category='error')
    return render_template(
        'guis/update/pet.html',
        query_options=[
            {"option": ["pet_name", "Pet Name"]},
            {"option": ["microchip", "Microchip Number"]},
            {"option": ["gender", "Gender"]},
            {"option": ["pet_type", "Pet Type"]},
            {"option": ["fixed", "Neutered/Spayed?"]},
            {"option": ["adopted", "Adopted?"]},
            {"option": ["adoption_date", "Adoption Date"]},
            {"option": ["shelter_name", "Shelter Name"]},
            {"option": ["birthday", "Year of Birth"]},
            {"option": ["colors", "Coloring"]},
            {"option": ["breed", "Breed"]},
            {"option": ["medical_record", "Current Medical Conditions"]},
            {"option": ["home_preference", "Home Preference"]},
            {"option": ["temperament", "Temperament"]},
            {"option": ["previously_adopted", "Previously Adopted?"]},
            {"option": ["reason_for_admittance", "Reason for Admittance"]}
        ]
    )

@bp.route('/shelter', methods=['GET', 'POST'])
@login_required
def shelter():
    error = None
    session_access = session.get('access')
    if (session_access == 'employee'):
        msg = 'Unauthorized operation for employees.'
        return redirect(url_for("employee.petSearch"))
    if (request.method == 'POST'):
        form_keys = request.form.keys()
        shelter_name = None
        if ('shelter_name' in form_keys):
            shelter_name = request.form["shelter_name"]
        city = None
        if ('city' in form_keys):
            city = request.form["city"]
        phone_number = None
        if ('phone_number' in form_keys):
            phone_number = request.form['phone_number']
        email = None
        if ('email' in form_keys):
            email = request.form['email'].lower()
        website = None
        if ('website' in form_keys):
            website = request.form['website'].lower()
        if (not shelter_name):
            error = 'Shelter name required.'
        if (error is None):
            db_num = hashName(shelter_name)
            db = databases[db_num]
            shelters = db["shelters"]
            subject_match = shelters.find_one({"name": shelter_name})
            if (subject_match is None):
                error = 'Shelter {} does not exist.'.format(shelter_name)
            else:
                attributes = {
                    "city": city,
                    "phone_number": phone_number,
                    "email": email,
                    "website": website
                }
                filtered_attributes = {key: value for key, value in attributes.items() if ((value != '') and (value is not None))}
                shelters.update_one({"name": shelter_name}, {"$set": filtered_attributes})
            if (error is None):
                flash('Success!', category='message')
                return redirect(url_for("dbm_query.dbm_query"))
    flash(error, category='error')
    return render_template(
        'guis/update/shelter.html',
        query_options=[
            {"option": ["shelter_name", "Shelter Name"]},
            {"option": ["city", "City"]},
            {"option": ["phone_number", "Phone Number"]},
            {"option": ["email", "Email"]},
            {"option": ["website", "Website"]}
        ]
    )