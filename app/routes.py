from flask import render_template, url_for, request, redirect, flash
from app import app, db
from app.models import User, Food
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm
#handlers for managing URLs

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username = current_user.username))
    form = LoginForm()            
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            pass_check = user.check_password(form.password.data)
            if pass_check: 
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('profile', username = current_user.username))
            else:
                flash('invalid password for this user')
                return redirect(url_for('login'))
        else: 
            flash('Invalid username')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username = form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('congratulations, welcome to my cult uwu')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', user=user)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        try:
            food_content = request.form['content']
            new_food = Food(groceryName=food_content)        
            db.session.add(new_food)
            db.session.commit()
            return redirect('/')
        
        except:
            flash("thats already on the list")
            return redirect('/')
    else:
        foods = Food.query.order_by(Food.data_created).all()
        return render_template('home.html', foods = foods)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/delete/<int:id>')
def delete(id):
    entry_to_delete = Food.query.get_or_404(id)

    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'oops'