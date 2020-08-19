from flask import render_template, url_for, request, redirect
from app import app
from app.models import User, Food
#handlers for managing URLs

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        food_content = request.form['content']
        new_food = Food(groceryName=food_content)

        try:
            db.session.add(new_food)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue with what you just tried'
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