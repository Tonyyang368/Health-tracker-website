from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groceryName = db.Column(db.String(200), unique=True, nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Food %r>' % self.id 


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)