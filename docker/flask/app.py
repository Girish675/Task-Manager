from flask import Flask, render_template, url_for, request, redirect
import random
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id

@app.route('/')
def index():
    images = [
        'images/image1.jpg',
        'images/image2.jpg',
        'images/image3.jpg',
        'images/image4.jpg',
        'images/image5.jpg',
        'images/image6.jpg',
        'images/image7.jpg',
        'images/image8.jpg',
        'images/image9.jpg',
        # Add paths to all 20 images
    ]
    selected_image = random.choice(images)
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks, background_image=selected_image)

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        task_content = request.form['content'].strip()  # Remove leading/trailing whitespace
        if task_content:  # Check if the content is not empty
            new_task = Todo(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There is an issue with adding the task, please check.'
        else:
            return redirect('/')  # Redirect back to the main page if the content is empty
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There is some problem while deleting the task. Please check.'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There is some problem while Updating the task. Please check.'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)