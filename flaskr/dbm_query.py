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

print('ready for querying')

bp = Blueprint('dbm_query', __name__, url_prefix='/dbm_query')
import create
bp.register_blueprint(create.bp)

import delete
bp.register_blueprint(delete.bp)

import update
bp.register_blueprint(update.bp)

import search
bp.register_blueprint(search.bp)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def dbm_query():
    session_access = session.get('access')
    if (session_access == 'employee'):
        msg = 'Unauthorized operation for employees.'
        return redirect(url_for("employee.petSearch"))
    if (request.method == 'POST'):
        query_type = request.form['query_select'].lower()
        subject_type = request.form['subject_select'].lower()
        if (query_type == 'select query type'):
            flash('Please select a valid query input.')
            return redirect(url_for('dbm_query.dbm_query'))
        elif (subject_type == 'subject'):
            flash('Please select a valid subject type.')
            return redirect(url_for('dbm_query.dbm_query'))
        else:
            print('waiting to redirect')
            return redirect(url_for('dbm_query.{}.{}'.format(query_type, subject_type)))
    print('query window')
    return render_template(
        'guis/db_manager.html',
        query_options=[
            {'query': 'Select Query Type'},
            {'query': 'Create'},
            {'query': 'Search'},
            {'query': 'Update'},
            {'query': 'Delete'}
        ],
        query_subjects=[
            {'subject': 'Subject'},
            {'subject': 'User'},
            {'subject': 'Pet'},
            {'subject': 'Shelter'}
        ]
    )