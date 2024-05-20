from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def __repr__(self) -> str:
        return f"{self.no} - {self.title}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)
@app.route('/show')
def products():
    alltodo=Todo.query.all()
    return 'My products'

@app.route('/update/<int:no>',methods=['GET','POST'])
def update(no):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo=Todo.query.filter_by(no=no).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit() 
        return redirect('/')
    todo=Todo.query.filter_by(no=no).first()
    return render_template('update.html', todo=todo)
@app.route('/delete/<int:no>')
def delete(no):
    todo=Todo.query.filter_by(no=no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8000)

def create_tables():
    with app.app_context():
        db.create_all()
        print("Tables created successfully.")
