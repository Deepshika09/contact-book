from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "secret123"

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Contact Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Contact {self.name}>"


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# Home Page
@app.route('/')
def home():
    return render_template('home.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            flash("Account already exists. Please login.")
            return redirect(url_for('login'))

        user = User(
            username=username,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for('login'))

    return render_template('register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:

            session['user_id'] = user.id
            session['username'] = user.username

            flash("Login successful!")
            return redirect(url_for('contacts'))

        flash("Invalid username or password.")

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():

    session.clear()

    flash("Logged out successfully.")
    return redirect(url_for('login'))


# View All Contacts
@app.route('/contacts')
def contacts():

    if 'user_id' not in session:
        flash("Please login first.")
        return redirect(url_for('login'))

    all_contacts = Contact.query.all()

    return render_template(
        'contacts.html',
        contacts=all_contacts
    )


# Add Contact
@app.route('/add', methods=['GET', 'POST'])
def add_contact():

    if 'user_id' not in session:
        flash("Please login first.")
        return redirect(url_for('login'))

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        new_contact = Contact(
            name=name,
            phone=phone,
            email=email
        )

        db.session.add(new_contact)
        db.session.commit()

        flash("Contact added successfully!")
        return redirect(url_for('contacts'))

    return render_template('add_contact.html')


# Contact Details
@app.route('/contact/<int:id>')
def contact_detail(id):

    if 'user_id' not in session:
        flash("Please login first.")
        return redirect(url_for('login'))

    contact = Contact.query.get_or_404(id)

    return render_template(
        'contact_detail.html',
        contact=contact
    )


# Edit Contact
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):

    if 'user_id' not in session:
        flash("Please login first.")
        return redirect(url_for('login'))

    contact = Contact.query.get_or_404(id)

    if request.method == 'POST':

        contact.name = request.form['name']
        contact.phone = request.form['phone']
        contact.email = request.form['email']

        db.session.commit()

        flash("Contact updated successfully!")
        return redirect(url_for('contacts'))

    return render_template(
        'edit_contact.html',
        contact=contact
    )


# Delete Contact
@app.route('/delete/<int:id>')
def delete_contact(id):

    if 'user_id' not in session:
        flash("Please login first.")
        return redirect(url_for('login'))

    contact = Contact.query.get_or_404(id)

    db.session.delete(contact)
    db.session.commit()

    flash("Contact deleted successfully!")
    return redirect(url_for('contacts'))


# Create Database Tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)