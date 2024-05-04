# dsci551-final-project
Commands for operation
- Start mongodb and create databases washelters1 and washelters2
- Use import_data.ipnyb to load data into database (locally)
- Start virtual environment in project folder with . .venv/bin/activate
- Run the app in the flaskr folder with flask run --debug
- Navigate to 127.0.0.1:5000 in your browser
- For database manager, login with username: chocoCat, password: dsci551
- Employee, login with username: donut, password: donutShop
- Fill out forms and see your results
File structure
- The project source code is found in the flaskr folder.
- The python script used to import the initial data is found in the import_data.ipynb file outside of the flaskr folder.
- app.py is used for routing the base pages of the application
- about.py was going to be used to create an about page for the website but was deemed unnecessary and thus not implemented.
- auth.py constructs the login page and connects to the database to verify user credentials.
- create.py deals with create operations on each collection in the databases.
- update.py deals with update operations on each collection in the databases.
- search.py deals with search operations for database manager queries on each collection in the databases.
- delete.py deals with delete operations on each collection in the databases.
- db_query.py loads the query selection page for the database manager.
- employee.py deals with pet search queries for employees.
- shelter_directory.py loads shelter information from the databases.
- The templates folder contains the html pages that display the information from the python scripts. It is organized with the following subfolders: auth and guis. The other html files are base.html and shelter_directory.html.
- The static folder contains files such as images and css files.
