# to handle all page routing
# routes will then render our html templates

from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, Leaves
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, LeaveRequestForm
from datetime import date

# index will route to our helper pages lea

@app.route('/') # route to index
@app.route('/index')
@login_required  # for use with login manager, to ensure still log in
def index():
    posts = "Welcome to leave scheduler !"
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
        user = User(username=form.username.data, email=form.email.data)
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
    posts = [
        {'author' : user, 'body' : 'Test post #1'},
        {'author' : user, 'body' : 'Test post #2'}
    ]
    # display the leave statistics
    # use this as a router to other pages

    return render_template('user_statistics.html', user = user, posts = posts)
    


@app.route('/user_statistics/<username>/leave_cancel', methods = ['GET','POST'])    
@login_required
def leave_cancel(username):
    # after confirmation, maybe can route to the statistics page
    # no need to generate form, will use the html template
    # once form is validated, we need to upadate the db for leaves of the user
    user = User.query.filter_by(username = username).first_or_404()
    leaves = user.leaves.order_by(Leaves.id.asc()).all()  
    return render_template('cancel.html', leaves = leaves, user = user, username = username)
#     leaves = Leave.query.filter_by(userid = user)


@app.route('/handle_data', methods = ['POST','GET'])
@login_required
def handle_data():
    
    # user = User.query.filter_by(username = current_user.username).first_or_404()
    path = request.form.getlist("returnthis")
    path = [int(p) for p in path] 
    # leaves = user.leaves.order_by(Leaves.id.asc()).all()  
    for p in path: #for id in list of ids
        delete_q = Leaves.query.get(p) #query by primary key
        db.session.delete(delete_q)
    db.session.commit()
    # delete_q = user.leaves.delete().where(user.leaves.id in path)
    # path returned successfully
    # need to update the leave request
    # user = User.query.filter_by(username = current_user.username).first_or_404()
    # for p in path:

    # leaves_to_del = user.leaves.filter_by(Leaves.id in path).all()
    # leaves = user.leaves.order_by(Leaves.id.asc()).all()  
    # print(leaves_to_del)
    flash('Leave request updated!')
    return(redirect('/user_statistics/{}'.format(current_user.username)))


@app.route('/user_statistics/<username>/leave_request', methods = ['GET', 'POST'])
@login_required
def leave_request(username):
    form = LeaveRequestForm()
    if form.validate_on_submit():
        leave = Leaves(startdate = form.startdate.data, enddate = form.enddate.data, note = form.note.data, halfdaybegin = form.halfdaybegin.data, halfdayend = form.halfdayend.data, employee = User.query.filter_by(username = username).first())
        db.session.add(leave)
        db.session.commit()
        flash("Leave request submitted")
        return redirect('/user_statistics/{}'.format(username)) # fill in the route
        # redirect()
    return render_template('leaverequest.html', title = "Leave Request", form = form)    


