from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Create the database tables before running the application
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Check if the name already exists in the database
        existing_user = User.query.filter_by(name=name).first()
        if existing_user:
            return 'Name already exists. Please use a different name.'

        # If the name doesn't exist, add the user to the database
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('hello', name=name))  # Redirect to hello route with the provided name
    return render_template('index.html')

@app.route('/hello/<name>')
def hello(name):
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(debug=True)






@app.route('/show_add_user', methods=['GET'])
def show_add_user_form():
    # This function will render the form template when visited with a GET request.
    return render_template('add_user_form.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    # This function will handle the form submission.
    # When the form is submitted, this function will be invoked to process the form data.
    name = request.form['name']
    email = request.form['email']
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return f'User {name} added successfully!'




@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    return '\n'.join([f'{user.name}: {user.email}' for user in users])
