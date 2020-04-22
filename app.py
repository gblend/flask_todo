
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
   id = db.column(db.Integer, primary_key=True)
   content = db.column(db.String(250), nullable=False)
   date_created = db.column(db.DateTime, default=datetime.utcnow)

   

@app.route('/')
def index():
   return render_template('index.html')


if __name__ == '__main__':
   app.run(debug=True)
