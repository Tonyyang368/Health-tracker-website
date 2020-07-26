from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#testing

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groceryName = db.Column(db.String(20), unique=True, nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id 


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

if __name__ == '__main__':
    app.run(debug=True)