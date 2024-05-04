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

bp = Blueprint('search', __name__, url_prefix='/search')

print('waiting to start search')

@bp.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    error = None
    session_access = session.get('access')
    if (session_access == 'employee'):
        msg = 'Unauthorized operation for employees.'
        return redirect(url_for("employee.petSearch"))
    form_submitted = False
    shelter_db1 = database1["shelters"]
    shelter_db2 = database2["shelters"]
    distinct_shelter1 = shelter_db1.distinct("name")
    distinct_shelter2 = shelter_db2.distinct("name")
    distinct_shelters = distinct_shelter1 + distinct_shelter2
    if (request.method == "POST"):
        form_submitted = True
        form_keys = request.form.keys()
        username = None
        if ('username' in form_keys):
            username = request.form["username"]
        first_name = None
        if ('first_name' in form_keys):
            first_name = request.form["first_name"]
        first_name_param = None
        if ('first_name_param' in form_keys):
            first_name_param = request.form["first_name_param"]
        last_name = None
        if ('last_name' in form_keys):
            last_name = request.form["last_name"]
        last_name_param = None
        if ('last_name_param' in form_keys):
            last_name_param = request.form["last_name_param"]
        shelter_name = None
        if ('shelter_name' in form_keys):
            shelter_name = request.form["shelter_name"]
        find_query = {}
        projection = {'username': 1, 'first_name': 1, 'last_name': 1, '_id': 0, 'shelter_id': 1, 'access_class': 1}
        shelter_id = None
        if (shelter_name):
            db_num = hashName(shelter_name)
            db = databases[db_num]
            shelter_result = db.shelters.find_one({"name": shelter_name})
            if (shelter_result):
                shelter_id = shelter_result["_id"]
                find_query["shelter_id"] = shelter_id
        if (username):
            find_query["username"] = username
        if ((first_name) and (first_name_param)):
            first_srch = {"${}".format(first_name_param): first_name}
            find_query["first_name"] = first_srch
        if ((last_name) and (last_name_param)):
            last_srch = {"${}".format(last_name_param): last_name}
            find_query["last_name"] = last_srch
        user_db1 = database1["users"]
        user_db2 = database2["users"]
        user_result1 = list(user_db1.find(find_query, projection))
        user_result2 = list(user_db2.find(find_query, projection))
        user_results = user_result1 + user_result2
        return render_template('guis/search/user.html', results_present=form_submitted, query_results=user_results)

    flash(error, category='error')
    return render_template('guis/search/user.html', results_present=form_submitted, shelter_list=distinct_shelters)

@bp.route('/pet', methods=['GET', 'POST'])
@login_required
def pet():
    print('search for pet')
    error = None
    session_access = session.get('access')
    if (session_access == 'employee'):
        msg = 'Unauthorized operation for employees.'
        return redirect(url_for("employee.petSearch"))
    form_submitted = False
    pet_db1 = database1["pets"]
    pet_db2 = database2["pets"]
    shelter_db1 = database1["shelters"]
    shelter_db2 = database2["shelters"]
    distinct_breed1 = pet_db1.distinct("breed")
    distinct_breed2 = pet_db2.distinct("breed")
    print('here')
    distinct_pet_type1 = pet_db1.distinct("pet_type")
    distinct_pet_type2 = pet_db2.distinct("pet_type")
    distinct_shelter1 = shelter_db1.distinct("name")
    distinct_shelter2 = shelter_db2.distinct("name")
    distinct_breeds = distinct_breed1 + distinct_breed2
    distinct_pet_types = distinct_pet_type1 + distinct_pet_type2
    distinct_shelters = distinct_shelter1 + distinct_shelter2
    if (request.method == "POST"):
        form_keys = request.form.keys()
        form_submitted = True
        pet_name = None
        if ('pet_name' in form_keys):
            pet_name = request.form['pet_name']
        name_param = None
        if ('name_param' in form_keys):
            name_param = request.form['name_param']
        microchip = None
        if ('microchip' in form_keys):
            microchip = request.form['microchip']
        gender = None
        if ('gender' in form_keys):
            gender = request.form['gender']
        pet_type = None
        if ('pet_type' in form_keys):
            pet_type = request.form['pet_type']
        color1 = None
        color2 = None
        color3 = None
        color4 = None
        color5 = None
        color6 = None
        color7 = None
        color8 = None
        color9 = None
        color10 = None
        color11 = None
        colors = [color1, color2, color3, color4, color5, color6, color7, color8, color9, color10, color11]
        color_options = ['color1', 'color2', 'color3', 'color4', 'color5', 'color6', 'color7', 'color8', 'color9', 'color10', 'color11']
        for i in range(len(color_options)):
            if (color_options[i] in form_keys):
                colors[i] = request.form[color_options[i]]
        breed = None
        if ('breed' in form_keys):
            breed = request.form['breed']
        fixed = None
        if ('fixed' in form_keys):
            fixed = request.form['fixed']
        adopted = None
        if ('adopted' in form_keys):
            adopted = request.form['adopted']
        adoption_date = None
        if ('adoption_date' in form_keys):
            adoption_date = request.form['adoption_date']
        adoption_param = None
        if ('adoption_param' in form_keys):
            adoption_param = request.form['adoption_param']
        shelter_name = None
        if ('shelter_name' in form_keys):
            shelter_name = request.form['shelter_name']
        birthday = None
        if ('birthday' in form_keys):
            birthday = request.form['birthday']
        age_param = None
        if ('age_param' in form_keys):
            age_param = request.form['age_param']
        home_preference1 = None
        home_preference2 = None
        home_preference3 = None
        home_preference4 = None
        home_preference5 = None
        home_preference6 = None
        home_preference7 = None
        home_preference8 = None
        home_preferences = [home_preference1, home_preference2, home_preference3, home_preference4,\
                            home_preference5, home_preference6, home_preference7, home_preference8]
        home_options = ['home_preference1', 'home_preference2', 'home_preference3', 'home_preference4',\
                        'home_preference5', 'home_preference6', 'home_preference7', 'home_preference8']
        for i in range(len(home_options)):
            home_keys = request.form.keys()
            if (home_options[i] in home_keys):
                home_preferences[i] = request.form[home_options[i]]
        temperament1 = None
        temperament2 = None
        temperament3 = None
        temperament4 = None
        temperament5 = None
        temperament6 = None
        temperament7 = None
        temperament8 = None
        temperament = [temperament1, temperament2, temperament3, temperament4, temperament5, temperament6,\
                       temperament7, temperament8]
        temperament_options = ['temperament1', 'temperament2', 'temperament3', 'temperament4', 'temperament5',\
                               'temperament6', 'temperament7', 'temperament8']
        for i in range(len(temperament_options)):
            temp_keys = request.form.keys()
            if (temperament_options[i] in temp_keys):
                temperament[i] = request.form[temperament_options[i]]
        previously_adopted = None
        if ('previously_adopted' in form_keys):
            previously_adopted = request.form['previously_adopted']

        if (birthday):
            birthday = datetime.strptime(birthday, '%Y-%m-%d')
        
        
        colors = [x for x in colors if x is not None]
        home_preferences = [x for x in home_preferences if x is not None]
        temperament = [x for x in temperament if x is not None]
        # formatting the find query
        # two queries for each database
        db1 = database1['pets']
        db2 = database2['pets']
        name_srch = None
        find_query = {}
        if ((pet_name) and (name_param)):
            if (name_param == 'equal_to'):
                name_srch = pet_name
            else:
                name_srch = {"$regex": pet_name, "$options": "i"}
            find_query["pet_name"] = name_srch
        shelter_id = None
        if (shelter_name):
            db_num = hashName(shelter_name)
            db = databases[db_num]
            shelter_result = db.shelters.find_one({"name": shelter_name})
            if (shelter_result):
                shelter_id = shelter_result["_id"]
                find_query["shelter_id"] = shelter_id
        if (colors):
            color_srch = {"$in": colors}
            find_query["colors"] = color_srch
        if (home_preferences):
            home_srch = {"$in": home_preferences}
            find_query["home_preference"] = home_srch
        if (temperament):
            temperament_srch = {"$in": temperament}
            find_query["temperament"] = temperament_srch
        if (microchip):
            find_query["microchip"] = microchip
        if (gender):
            find_query["gender"] = gender
        if (pet_type):
            find_query["pet_type"] = pet_type
        if (breed):
            find_query["breed"] = breed
        if (fixed):
            if (fixed == "True"):
                find_query["fixed"] = True
            else:
                find_query["fixed"] = False
        if (adopted):
            if (adopted == "True"):
                find_query["fixed"] = True
            else:
                find_query["fixed"] = False
        if (previously_adopted):
            if (previously_adopted == "True"):
                find_query["previously_adopted"] = True
            else:
                find_query["previously_adopted"] = False
        if ((birthday) and (age_param)):
            age_srch = {"${}".format(age_param): birthday}
            find_query["birthday"] = age_srch
        if ((adoption_date) and (adoption_param)):
            adoption_srch = {"${}".format(adoption_param): adoption_date}
            find_query["adoption_date"] = adoption_srch
        db1_result = list(db1.find(find_query))
        db2_result = list(db2.find(find_query))
        # combine the two db results
        results = db1_result + db2_result

        return render_template('guis/search/pet.html', results_present=form_submitted, query_results=results)
    flash(error, category='error')
    print('loading srch page')
    return render_template(
        'guis/search/pet.html',
        results_present=form_submitted,
        breed_list=distinct_breeds,
        shelter_list=distinct_shelters,
        pet_type_list=distinct_pet_types
    )

@bp.route('/shelter', methods=['GET', 'POST'])
@login_required
def shelter():
    session_access = session.get('access')
    if (session_access == 'employee'):
        msg = 'Unauthorized operation for employees.'
        return redirect(url_for("employee.petSearch"))
    error = None
    form_submitted = False
    shelter_db1 = database1["shelters"]
    shelter_db2 = database2["shelters"]
    distinct_shelter1 = shelter_db1.distinct("name")
    distinct_shelter2 = shelter_db2.distinct("name")
    distinct_shelters = distinct_shelter1 + distinct_shelter2
    if (request.method == "POST"):
        form_submitted = True
        form_keys = request.form.keys()
        shelter_name = None
        if ('shelter_name' in form_keys):
            shelter_name = request.form["shelter_name"]
        city = None
        if ('city' in form_keys):
            city = request.form["city"]
        find_query = {}
        if (shelter_name):
            find_query["name"] = shelter_name
        if (city):
            find_query["city"] = city
        print(shelter_name)
        print(find_query)
        srch_result1 = list(shelter_db1.find(find_query))
        srch_result2 = list(shelter_db2.find(find_query))
        srch_results = srch_result1 + srch_result2
        print(srch_results)
        return render_template('guis/search/shelter.html', results_present=form_submitted, query_results=srch_results)
    flash(error, category='error')
    return render_template('guis/search/shelter.html', results_present=form_submitted, shelter_list=distinct_shelters)