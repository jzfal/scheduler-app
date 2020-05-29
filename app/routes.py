# to handle all page routing
# routes will then render our html templates

from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, Leaves, PublicHolidays, Admins
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, LeaveRequestForm, PublicHolidaysForm, UserSearchForm
from datetime import date

# index will route to our helper pages lea

@app.route('/') # route to index
@app.route('/index')
@login_required  # for use with login manager, to ensure still log in
def index():
    posts = "Welcome to leave scheduler !"

    # if current_user.is_administrator:


    return render_template('index.html', title = 'Home', posts = posts)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated: # alr authenticated can route to other pages
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): # when POST request
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login')) # can redirect to another page such as leave request
        login_user(user, remember= form.remember_me.data) # register user as logged in, current user = user
        next_page = request.args.get('next') # if user was redirected, capture the 'next' page, the page user was on before redirect
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Sign In', form = form)


@app.route('/logout')
def logout():
    """if logged in , then log in template switch to log out"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.username.data in Admins.Admin_ls:
            admin = True
        else:
            admin = False
        user = User(username=form.username.data, admin = admin)
        print(admin)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user_statistics/<username>', methods = ['GET','POST'])
@login_required
def user_statistics(username):
    user = User.query.filter_by(username = username).first_or_404()
    leaves = user.leaves.order_by(Leaves.id.asc()).all()
    # display the leave statistics
    # use this as a router to other pages
    # leaves is a list, index is the leaves id

    mod_leaves = [] 
    approved_days = 0
    for i in range(len(leaves)):
        working_days = count_num_leaves(leaves[i].startdate,leaves[i].enddate, leaves[i].halfdayend,leaves[i].halfdaybegin)
        mod_leaves.append({'leave_id':leaves[i].id,'startdate':leaves[i].startdate, 'enddate': leaves[i].enddate, 'TotalDays':working_days, "Status": leaves[i].status})
        if leaves[i].status == "Approved" or leaves[i].status == "Canceling":
            # have to log this in the admin side, canceling still counts to annual leave, need to wait for admin to change to cancel
            approved_days += working_days
    number_of_leaves_remaining = 15 - approved_days # take this minus the number of days that have approved leaves
    return render_template('user_statistics.html', user = user, mod_leaves = mod_leaves, number_of_leaves_remaining = number_of_leaves_remaining)
    


@app.route('/user_statistics/<username>/leave_cancel', methods = ['GET','POST'])    
@login_required
def leave_cancel(username):
    # after confirmation, maybe can route to the statistics page
    # no need to generate form, will use the html template
    # once form is validated, we need to upadate the db for leaves of the user
    user = User.query.filter_by(username = username).first_or_404()
    leaves = user.leaves.order_by(Leaves.id.asc()).all()  
    mod_leaves = [] 
    approved_days = 0
    for i in range(len(leaves)):
        # print(leaves[i].status)
        if leaves[i].status == "Approved" or leaves[i].status ==  "Created": 
            # approved status only by admin
            working_days = count_num_leaves(leaves[i].startdate,leaves[i].enddate, leaves[i].halfdayend,leaves[i].halfdaybegin)

            mod_leaves.append({'leave_id':leaves[i].id,'startdate':leaves[i].startdate, 'enddate': leaves[i].enddate, 'TotalDays':working_days, "Status": leaves[i].status})
        else:
            continue

    return render_template('cancel.html', leaves = mod_leaves, user = user, username = username)


@app.route('/handle_data', methods = ['POST','GET'])
@login_required
def handle_data():
    """
    this view is linked to cancelling leave view for user
    """
    # user = User.query.filter_by(username = current_user.username).first_or_404()
    path = request.form.getlist("returnthis")
    for p in path:
        # will return status,leave_id
        curr_status = p.split(',')[0]
        curr_leaveid = p.split(',')[1]
        if curr_status == 'Created':
            delete_q = Leaves.query.get(curr_leaveid) #query by primary key
            db.session.delete(delete_q)
        elif curr_status == 'Approved':
            # the case where curr status is Approved
            q = Leaves.query.get(curr_leaveid)
            q.status = 'Canceling'
    db.session.commit()

    flash('Leave request updated!')
    return(redirect('/user_statistics/{}'.format(current_user.username)))


@app.route('/user_statistics/<username>/leave_request', methods = ['GET', 'POST'])
@login_required
def leave_request(username):
    form = LeaveRequestForm()
    if form.validate_on_submit():
        leave = Leaves(startdate = form.startdate.data, enddate = form.enddate.data, note = form.note.data, halfdaybegin = form.halfdaybegin.data, halfdayend = form.halfdayend.data, employee = User.query.filter_by(username = username).first(), status = "Created")
        db.session.add(leave)
        db.session.commit()
        flash("Leave request submitted")
        return redirect('/user_statistics/{}'.format(username)) # fill in the route
        # redirect()
    return render_template('leaverequest.html', title = "Leave Request", form = form)    


##### Admin views

@app.route('/holidays_list', methods = ["GET", "POST"])
@login_required
def holidays_list():
    """
    editable table of holidays, admin is able to cancel the holidays
    """
    publicholidays = PublicHolidays.query.order_by(PublicHolidays.date.asc()).all() 
    public_holidays = [] 
    approved_days = 0
    for i in range(len(publicholidays)):
        public_holidays.append({'holiday_id':publicholidays[i].id,'date':publicholidays[i].date, 'name': publicholidays[i].name})

    return render_template('edit_holiday.html', holiday = public_holidays, username = current_user.username)


@app.route('/public_holiday', methods = ["GET", "POST"])
@login_required
def public_holiday():
    """
    admin view to add new holidays, need validation !
    """
    form = PublicHolidaysForm()
    if form.validate_on_submit():
        public_holiday = PublicHolidays(name = form.name.data, date = form.date.data)
        db.session.add(public_holiday)
        db.session.commit()
        flash("Public Holiday Added !")
        return redirect(url_for('holidays_list')) # add url to list of public holidays
    return render_template('addholiday.html', title = 'Add holiday', form = form, username = current_user.username)


@app.route('/all_leave_request', methods = ["GET", "POST"])
@login_required
def all_leave_request():
    """
    admin view to view all leave request and take action

    if request exceeds capacity, must highlight !
    """
    user = User.query.all()
    pendings = []
    for u  in user:
        if u.is_administrator():
            continue # remove all admins
        else:
            curr_user = u.username
            curr_id = u.id
            # find out the current leave statistic of this user 
            total_approved = count_total_leaves(u)
            leaves = u.leaves.order_by(Leaves.id.asc()).all()
            for leave in leaves:
                curr_startdate = leave.startdate
                curr_enddate = leave.enddate
                curr_halfdaybegin = leave.halfdaybegin
                curr_halfdayend = leave.halfdayend
                curr_totaldays = count_num_leaves(curr_startdate, curr_enddate,curr_halfdayend,curr_halfdaybegin)
                curr_status = leave.status
                curr_leaveid = leave.id
                curr_exceed = (total_approved + curr_totaldays) > 15
                if curr_status in ('Rejected', 'Approved', 'Canceled'): 
                    # for this status admin does not need to approve
                    continue

                pendings.append({'username':curr_user,
                                'leaveid':curr_leaveid,
                                'startdate':curr_startdate,
                                'enddate':curr_enddate,
                                'starthalf': curr_halfdaybegin,
                                'endhalf': curr_halfdayend,
                                'TotalDays': curr_totaldays,
                                'Status': curr_status,
                                'Exceed': curr_exceed})

    return render_template('all_leave_request.html', pendings = pendings, username = current_user.username)

@app.route('/all_user_statistics_search', methods = ["GET","POST"])
@login_required
def all_user_statistics_search():
    """
    no action required on this page
    extracts all user statistics 
    user_id, username, 
    
    admin inputs user name, and redirect to that users statistics
    """
    form = UserSearchForm()
    return render_template('all_user_statistics_search.html', form = form)




@app.route('/all_user_statistics', methods = ["GET","POST"])
@login_required
def all_user_statistics():
    name = request.form['name']
    user = User.query.filter_by(username = name).first_or_404()
    leaves = user.leaves.order_by(Leaves.id.asc()).all()
    if len(leaves) == 0:
        flash("No results found")
        return redirect(url_for('all_user_statistics_search'))

    mod_leaves = [] 
    approved_days = 0
    for i in range(len(leaves)):
        working_days = count_num_leaves(leaves[i].startdate,leaves[i].enddate, leaves[i].halfdayend,leaves[i].halfdaybegin)
        mod_leaves.append({'leave_id':leaves[i].id,'startdate':leaves[i].startdate, 'enddate': leaves[i].enddate, 'TotalDays':working_days, "Status": leaves[i].status})
        if leaves[i].status == "Approved" or leaves[i].status == "Canceling":
            approved_days += working_days
    number_of_leaves_remaining = 15 - approved_days # take this minus the number of days that have approved leaves
    return render_template('all_user_statistics.html', user = user,
                            mod_leaves = mod_leaves,
                            number_of_leaves_remaining = number_of_leaves_remaining)






@app.route('/handle_all_leave_data', methods = ['POST','GET'])
@login_required
def handle_all_leave_data():
    """
    main duties are to write the database to change the status of the 
    leave request
    """    
    path = request.form.getlist("action")
    for p in path: 
        new_status = p.split(',')[0] # new status by admin
        curr_leave_id = p.split(',')[1] # leave id of corresponding status
        if new_status == 'Empty':
            # allow admin to delay approval
            continue
        else:
            # if status is rejected, then remove from admin view
            update_q = Leaves.query.get(curr_leave_id)
            update_q.status = new_status
        db.session.commit()
    flash('Leave status has been updated')
    return(redirect(url_for('all_leave_request')))




@app.route('/handle_all_data', methods = ['POST','GET'])
@login_required
def handle_all_data():
    """
    this view is linked to handling holidaylist
    """
    path = request.form.getlist("returnthis1")  
    for p in path: #for id in list of ids
        delete_q = PublicHolidays.query.get(p) #query by primary key
        db.session.delete(delete_q) 
    db.session.commit()
    flash('Holiday List updated!')
    return(redirect(url_for('holidays_list')))











#### Utility

def count_num_leaves(start_dt, end_dt, halfdayend, halfdaybegin):
    """
    Helper function to calculate number of work days
    
    """
    # get the list of public holidays
    publicholidays = PublicHolidays.query.order_by(PublicHolidays.date.asc()).all() # this is the base query object
    holiday_dates = [p.date for p in publicholidays]
    
    
    
    # day counting logic
    num_days = (end_dt -start_dt).days +1
    num_weeks =(num_days)//7
    a=0
    # condition 1
    if end_dt.strftime('%a')=='Sat':
        if start_dt.strftime('%a') != 'Sun':
            a= 1
    # condition 2
    if start_dt.strftime('%a')=='Sun':
        if end_dt.strftime('%a') !='Sat':
            a =1
    # condition 3
    if end_dt.strftime('%a')=='Sun':
        if start_dt.strftime('%a') not in ('Mon','Sun'):
            a =2
    # condition 4        
    if start_dt.weekday() not in (0,6):
        if (start_dt.weekday() -end_dt.weekday()) >=2:
            a =2
    working_days =num_days -(num_weeks*2)-a

    less = 0

    # half day logic 
    if halfdayend or halfdaybegin:
        if halfdaybegin and halfdayend:
            less += 1
        else:
            less += 0.5

    # logic for when holiday is in the range of working days and holiday is not a weekend

    holidays_counter = 0

    for date in holiday_dates:
        if (start_dt <= date <= end_dt) and (date.weekday() not in (5,6)):
            # checks if the date is in the leave interval and if it is a weekday
            holidays_counter += 1


    return working_days - less - holidays_counter
        





def count_total_leaves(user):
    """
    given the user, return the total number of approved leaves
    user is an object of class User
    """
    approved_days = 0
    leaves = user.leaves.order_by(Leaves.id.asc()).all()
    for leave in leaves:
        if leave.status == "Approved":
            approved_days += count_num_leaves(leave.startdate,
                                            leave.enddate,
                                            leave.halfdaybegin,
                                            leave.halfdayend)
    
    return approved_days




