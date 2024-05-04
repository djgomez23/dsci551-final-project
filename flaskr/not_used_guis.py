from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from flaskr.auth import login_required

bp = Blueprint('guis', __name__)

@bp.route('/index/<access>')
@login_required
def index(access):
    return render_template('guis/index.html', user_access=access)

@bp.route('/db_manager', methods=('GET', 'POST'))
@login_required
def db_manager():
    return render_template('guis/db_manager.html',
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

@bp.route('/employee', methods=('GET', 'POST'))
@login_required
def employee():
    return render_template('guis/employee.html')
