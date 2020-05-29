# DTL Web Developer Project Assessment 

## Architecture of Web Application

## Instructions on how to run the Web Application 


### Setting of development server 
- Use the flag `set FLASK_APP=main.py`
- To run in development env run command `set FLASK_ENV=development`


### config module
- For seperation of concerns different configuration setups


### upgrade db
- When upgrading db run the migrate function with flask `flask db migrate -m "posts table"` followed by `flask db upgrade` to upgrade the database. Possible to downgrade the database as well

## Errors
#### Error in flask_shell
- when set to development enviroment, name error is raised in `flask shell`

#### Error when creating instance of Leaves 
- the name of the foreign key has to be the same as the backref

#### Join errors
- Refer to each user model and then request for leaves model


#### Search error
- Whenever a new user joins, the search form is not updated automatically
## To Do:
- For cancelling, need to add in checker for approve status, approve status can only be given by the admin (done)
- For admin account, need dbmodel and form for editing the list of public holidays (done)
- Remove email field from registration (done)
- need to handle the status where user is in the midst of leave, and wants to cancel leave (done)
    - need to address the cancelling state, where status is originally "Approved" (done)
- In order to activate admin, must create user from regristration page, do not create admin user from shell as admin rights is granted at registration (done)
- Check date validation for inputing new holidays (done)
- Need to validate leave request by name(done) 
- Validate leave request form  (done)
    - For leave statistics, need to update with the other status plus need take into account public holidays (done) 
- Admin needs a leave statistic view to see all user leave statistics
- Admin when approving leave needs to be able to see "request exceeds capacity", add into template "all_leave_request" (done)
- Need to add in logic for when a user cancels their approved leave requests at a time after the start date, this will flag up as `status == Canceling`. (done)
- Add data validation for leave request, if start or end date is a holiday, then flash error (done)
- Update id for all html tables, just show a counter instead of the actual primarykey



### Test simple user routines
- When admin approve leave, leave statistic should change
- When admin approve leave, and user cancel leave, status should change to 'Canceling', do not delete entry, leave days remaining should remain unchanged, once admin rejects then delete entry, revise leave statistic


### Test simple admin routines


### Latest App Updates

- Data Models intact
- Admin registration must be done through registration form
- Adding new holiday and removing existing holiday in order
- UNABLE TO RESOLVE INNER JOIN TO SHOW ALL THE LEAVE REQUEST (resolved)
- Admin able to approve request
- All forms intact


### Resource list 
- [multiple validators](https://stackoverflow.com/questions/21815067/how-do-i-validate-wtforms-fields-against-one-another)
- [flask blogging tutorial](https://stackoverflow.com/questions/21815067/how-do-i-validate-wtforms-fields-against-one-another)



