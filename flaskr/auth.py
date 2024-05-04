import functools
# need to use this to generate the hash for passwords at some point
# like when a new user is created
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import config
from pymongo import MongoClient
# client = MongoClient("mongodb://{}:{}@{}".format(config["username"], config["password"], config["ip_address"]))
client = MongoClient("localhost", 27017)
# if name length is odd, database1
database1 = client['washelters1']
# if name length is even, database2
database2 = client['washelters2']
databases = [database1, database2]

# from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def hashUsername(username):
    db_num = len(username) % 2
    return db_num

@bp.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    valid = False
    if (request.method == 'POST'):
        print('checking')
        username = request.form['username']
        password = request.form['password']
        print(username)
        # hash the username to find the database
        db_num = hashUsername(username)
        database = databases[db_num]
        users = database['users']
        # check if the username and password exist
        user = users.find_one({'username': username})
        match = check_password_hash(pwhash=user['password'], password=password)
        if (match):
            msg = 'Login successful.'
            valid = True
        else:
            print('error!')
            msg = 'Invalid username or password. Please try again.'

        if (valid):
            session.clear()
            session['username'] = user['username']
            session['access'] = user['access_class']
            session_access = session['access']
            print(session)
            flash(msg)
            if (session_access == 'employee'):
                session['page'] = 'employee.petSearch'
                return redirect(url_for('employee.petSearch'))
            else:
                print('welcome admin')
                session['page'] = 'dbm_query.dbm_query'
                return redirect(url_for('dbm_query.dbm_query'))
        flash(msg)
    return render_template('auth/login.html', msg=msg)

@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')
    # username = session.get('username')
    # db_num = hashUsername(username)
    # database = databases[db_num]
    # users = database['users']
    # print('session user: ' + str(user_id))
    
    if username is None:
        g.user = None
    else:
        db_num = hashUsername(username)
        database = databases[db_num]
        users = database['users']
        print(username)
        g.user = users.find_one({'username': username})

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        elif ((session.get('access') == 'employee') and (session.get('page') != 'employee.petSearch')):
            flash('Unauthorized operation')
            return redirect(url_for('employee.petSearch'))

        return view(**kwargs)

    return wrapped_view
