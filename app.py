
from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'developement key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# Database model
class Todo(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   content = db.Column(db.String(250), nullable=False)
   date_created = db.Column(db.DateTime, default=datetime.utcnow)

   def __repr__(self):
      return '<Task %r>' % self.id

   
@app.route('/')
def index():
   tasks = Todo.query.order_by(Todo.date_created).all()
   return render_template('index.html', tasks = tasks)


# Create todo
@app.route('/create', methods=['POST', 'GET'])
def create_todo():
   if request.method == 'POST':
      if not request.form['content']:
         msg = flash('Please fill in task description', 'error')
         return render_template('create.html', msg = msg)
      elif len(request.form['content']) < 5:
         msg = flash('Task description is too short', 'error')
         return render_template('create.html', msg = msg)
      else:
         task_content = request.form['content']
         new_task = Todo(content=task_content)

      try:
         db.session.add(new_task)
         db.session.commit()
         msg = flash('Task added successfully', 'success')
         return render_template('create.html', msg = msg)
      except: 
         return flash('There was an issue adding your task', 'error')
   else:
      return render_template('create.html')


# Delete todo
@app.route('/delete/<int:id>')
def delete_todo(id):
   task_to_delete = Todo.query.get_or_404(id)

   try:
      db.session.delete(task_to_delete)
      db.session.commit()
      return redirect('/')
   except: 
      msg = flash('There was a problem deleting this task', 'error')
      return render_template('index.html', msg=msg)


# Update todo detail
@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update_todo(id):
   if request.method == 'POST':
      taskID_to_update = Todo.query.get_or_404(id)
      if not request.form['content']:
         msg = flash('Please fill in task detail', 'error')
         return render_template('update.html', msg = msg)
      else:
         taskID_to_update.content = request.form['content']
      try:
         db.session.commit()
         return redirect('/')
   
      except:
         msg = flash('There was a problem updating this task')
   else:
      taskID_to_update = Todo.query.get_or_404(id)
      return render_template('update.html', task = taskID_to_update)


if __name__ == '__main__':
   app.run(debug=True)