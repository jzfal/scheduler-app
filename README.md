# DTL Web Developer Project Assessment 




## Architecture of Web Application

## Instructions on how to run the Web Application 


### Setting of development server 
- Use the flag `set FLASK_APP=main.py`
- To run in development env run command `set FLASK_ENV=development`


### config module
- For seperation of concerns


### upgrade db
- When upgrading db run the migrate function with flask `flask db migrate -m "posts table"` followed by `flask db upgrade` to upgrade the database. Possible to downgrade the database as well


### Error in flask_shell
- when set to development enviroment, name error is raised in `flask shell`

### Error when creating instance of Leaves 
the name of the foreign key has to be the same as the backref