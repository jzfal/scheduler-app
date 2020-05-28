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

### TO DO 
- Viewing the list of leave request (show status) for users
- Seeing their own leaving statistic
    - Leave left: Number of days left of annual leave

#### for admin
- editable list of public holidays of a specific year
- reject or approve a leave request
    - every leave request needs admins approval
    - when a user cancels their approved leave request in mid of the period it needs to be approve by an administrator

- Veiwing all peoples leave requests and statistics


#### other requirements
- Annual leave is always 15 days
- Leave request states


### todo:
- For cancelling, need to add in checker for approve status, approve status can only be given by the admin
- For leave statistics, need to update with the other status plus need take into account public holidays
- For admin account, need dbmodel and form for editing the list of public holidays

