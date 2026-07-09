from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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


# Home Page
@app.route('/')
def home():
    return render_template('home.html')


# View All Contacts
@app.route('/contacts')
def contacts():

    all_contacts = Contact.query.all()

    return render_template(
        'contacts.html',
        contacts=all_contacts
    )


# Add Contact
@app.route('/add', methods=['GET', 'POST'])
def add_contact():

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

        return redirect(url_for('contacts'))

    return render_template('add_contact.html')


# Contact Details
@app.route('/contact/<int:id>')
def contact_detail(id):

    contact = Contact.query.get_or_404(id)

    return render_template(
        'contact_detail.html',
        contact=contact
    )


# Delete Contact
@app.route('/delete/<int:id>')
def delete_contact(id):

    contact = Contact.query.get_or_404(id)

    db.session.delete(contact)
    db.session.commit()

    return redirect(url_for('contacts'))


# Create Database Tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)