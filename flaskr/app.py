import os
import config

from flask import Flask, request, render_template, session, redirect, url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = config.flask_secret

@app.route('/')
def welcome(): 
    return render_template("base.html")
  
import auth
app.register_blueprint(auth.bp)

#from . import guis
#app.register_blueprint(guis.bp)
#app.add_url_rule('/', endpoint='index')

import dbm_query
app.register_blueprint(dbm_query.bp)
app.add_url_rule('/', endpoint='index')

import employee
app.register_blueprint(employee.bp)
app.add_url_rule('/', endpoint='index')

import shelter_directory
app.register_blueprint(shelter_directory.bp)

if __name__ == "__main__": 
    app.run(debug=True)