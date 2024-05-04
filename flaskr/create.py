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

bp = Blueprint('create', __name__, url_prefix='/create')

# create user
@bp.route('/user', methods=['GET', 'POST'])
@login_required
# this will be like the register page from the tutorial
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
        shelter_name = None
        if ('shelter_name' in form_keys):
            shelter_name = request.form["shelter_name"]
        password = None
        if ('password' in form_keys):
            password = request.form['password']
        access_class = None
        if ('access_class' in form_keys):
            access_class = request.form['access_class'].lower()
        
        if (not username):
            error = 'Username required.'
        elif (not password):
            error = 'Password required.'
        elif (not access_class):
            error = 'Access class required.'
        elif (not shelter_name):
            error = 'Shelter name required.'
        if (error is None):
            # hash the username to find the appropriate database
            db_num = hashName(username)
            db = databases[db_num]
            # check if the username already exists
            users = db["users"]
            subject_match = users.find_one({"username": username})
            # if the username does exist, error = 'User {} already exists. Please pick another.'.format(username)
            if (subject_match):
                error = 'User {} already exists. Please pick another'.format(username)
            # if it doesn't, generate a hash for the password and enter the user information into the db
            # including the user access level
            else:
                hashed_pass = generate_password_hash(password)
                shelter_db_num = hashName(shelter_name)
                shelter_db = databases[shelter_db_num]
                shelter = shelter_db["shelters"].find_one({"name": shelter_name})
                # check to see if the shelter exists
                if (shelter is None):
                    error = "Please enter a valid shelter name or add a new shelter to the database."
                else:
                    shelter_id = shelter["_id"]
                    
                    attributes = {
                        "username": username,
                        "password": hashed_pass,
                        "access_class": access_class,
                        "first_name": first_name,
                        "last_name": last_name,
                        "shelter_id": shelter_id
                    }
                    filtered_attributes = {key: value for key, value in attributes.items() if ((value != '') and (value is not None))}
                    users.insert_one(filtered_attributes)
            # if no errors, flash('Success!), redirect(url_for("guis.db_manager")) to reload the query options
            if (error is None):
                flash('Success!', category='message')
                return redirect(url_for("dbm_query.dbm_query"))
                
    # if error, flash(error), render_template("dbm_query/create.html", subject=subject)
    flash(error, category='error')
    return render_template(
        "guis/create/user.html",
        query_options=[
            {"option": ["username", "Username"]},
            {"option": ["password", "Password"]},
            {"option": ["access_class", "Access Class (employee or db_manager)"]},
            {"option": ["first_name", "First Name"]},
            {"option": ["last_name", "Last Name"]},
            {"option": ["shelter_name", "Animal Shelter of Employment"]}
        ]
    )

@bp.route('/pet', methods=['GET', 'POST'])
@login_required
# this will be like the register page from the tutorial
def pet():
    session_access = session.get('access')
    if (session_access == 'employee'):
        msg = 'Unauthorized operation for employees.'
        return redirect(url_for("employee.petSearch"))
    error = None
    if (request.method == 'POST'):
        print('answers posted')
        form_keys = request.form.keys()
        print(form_keys)
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
        birthday_day = None
        if ('birthday_day' in form_keys):
            birthday_day = request.form['birthday_day']
        birthday_month = None
        if ('birthday_month' in form_keys):
            birthday_month = request.form['birthday_month']
        birthday_year = None
        if ('birthday_year' in form_keys):
            birthday_year = request.form['birthday_year']
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
            error = 'Please name the pet.'
        elif (not microchip):
            error = 'Please enter a valid microship number.'
        elif (not gender):
            error = 'Please enter the gender of the pet.'
        elif (not pet_type):
            error = 'Please indicate the type of pet'
        elif (not shelter_name):
            error = 'Please enter the shelter that the pet is residing/resided at.'
        elif (not adopted):
            error = 'Please indicate whether the pet has been adopted or not.'
        print(error)
        if (error is None):
            # hash by the pet's name
            db_num = hashName(pet_name)
            db = databases[db_num]
            pets = db["pets"]
            # check if the pet exists already through their microship number
            pet_match = pets.find_one({"microchip": microchip})
            if (pet_match):
                error = 'A pet with the microchip number {} already exists.'.format(microchip)
                print(error)
            else:  
            # if the pet does not exist already, find the shelter id
                print('almost there')
                shelter_db_num = hashName(shelter_name)
                shelter_db = databases[shelter_db_num]
                shelter = shelter_db["shelters"].find_one({"name": shelter_name})
                # check to see if the shelter exists
                if (shelter is None):
                    error = "Please enter a valid shelter name or add a new shelter to the database."
                else:
                    shelter_id = shelter["_id"]
                    color_list = None
                    home_list = None
                    temperament_list = None
                    if (colors):
                        color_list = colors.split(', ')
                    if (home_preference):
                        home_list = home_preference.split(', ')
                    if (temperament):
                        temperament_list = temperament.split(', ')
                    # birthday = datetime.datetime(int(birthday_year), int(birthday_month), int(birthday_day))
                    birthday = None
                    if (birthday_year and birthday_month and birthday_day):
                        birthday = '{0}-{1}-{2}'.format(str(birthday_year), str(birthday_month).zfill(2), str(birthday_day).zfill(2))
                    if (adoption_date):
                        adoption_date = datetime.datetime.strptime(adoption_date, '%Y-%m-%d')
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
                        "pet_name": pet_name,
                        "microchip": int(microchip),
                        "gender": gender,
                        "pet_type": pet_type,
                        "fixed": fixed,
                        "adopted": adopted,
                        "adoption_date": adoption_date,
                        "shelter_id": shelter_id,
                        "birthday": birthday,
                        "colors": color_list,
                        "breed": breed,
                        "medical_record": medical_record,
                        "home_preference": home_list,
                        "temperament": temperament_list,
                        "previously_adopted": previously_adopted,
                        "reason_for_admittance": reason_for_admittance
                    }
                    # enter the pet information into the appropriate database
                    print(attributes)
                    filtered_attributes = {key: value for key, value in attributes.items() if ((value != '') and (value is not None))}
                    print(filtered_attributes)
                    pets.insert_one(filtered_attributes)

            if (error is None):
                flash('Success!', category='message')
                return redirect(url_for("dbm_query.dbm_query"))
                
    # if error, flash(error), render_template("dbm_query/create.html", subject=subject)
    flash(error, category='error')
    return render_template(
        "guis/create/pet.html",
        query_options=[
            {"option": ["pet_name", "Pet Name"]},
            {"option": ["microchip", "Microchip Number"]},
            {"option": ["gender", "Gender"]},
            {"option": ["pet_type", "Pet Type (i.e. dog, cat, rabbit)"]},
            {"option": ["fixed", "Neutered/Spayed? (True or False)"]},
            {"option": ["adopted", "Adopted? (True or False)"]},
            {"option": ["adoption_date", "Adoption Date (yyyy-mm-dd)"]},
            {"option": ["shelter_name", "Shelter Name"]},
            {"option": ["birthday_year", "Year of Birth"]},
            {"option": ["birthday_month", "Month of Birth (number 1-12)"]},
            {"option": ["birthday_day", "Day of Birth"]},
            {"option": ["colors", "Coloring (comma separated list such as 'black, white')"]},
            {"option": ["breed", "Breed"]},
            {"option": ["medical_record", "Current Medical Conditions"]},
            {"option": ["home_preference", "Home Preference (comma separated list such as 'quiet, kids okay')"]},
            {"option": ["temperament", "Temperament (comma separated list such as 'playful, anxious')"]},
            {"option": ["previously_adopted", "Previously Adopted? (true or false)"]},
            {"option": ["reason_for_admittance", "Reason for Admittance (i.e., abandoned, stray, surrendered, etc.)"]}
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
        print('loading request')
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
            error = 'Please provide the name of the shelter.'
        elif (not city):
            error = 'Please provide the city where the shelter is located.'
        else:
            if (error is None):
                db_num = hashName(shelter_name)
                db = databases[db_num]
                shelters = db['shelters']
                shelter_match = shelters.find_one({"name": shelter_name})
                if (shelter_match):
                    error = 'A shelter with the name {} already exists.'.format(shelter_name)
                else:
                    attributes = {
                        "name": shelter_name,
                        "city": city,
                        "phone_number": phone_number,
                        "email": email,
                        "website": website
                    }
                
                    filtered_attributes = {key: value for key, value in attributes.items() if ((value != '') and (value is not None))}
                    print(filtered_attributes)
                    shelters.insert_one(filtered_attributes)
                print(error)
                if (error is None):
                    flash('Success!', category='message')
                    return redirect(url_for("dbm_query.dbm_query"))
    flash(error, category='error')
    return render_template(
        'guis/create/shelter.html',
        query_options=[
            {"option": ["shelter_name", "Shelter Name"]},
            {"option": ["city", "City"]},
            {"option": ["phone_number", "Phone Number"]},
            {"option": ["email", "Email"]},
            {"option": ["website", "Website"]}
        ]
    )