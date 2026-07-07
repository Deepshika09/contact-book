from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect('contacts.db')
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contacts')
def contacts():

    conn = sqlite3.connect('contacts.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    all_contacts = cur.fetchall()

    conn.close()

    return render_template(
        'contacts.html',
        contacts=all_contacts
    )


@app.route('/add', methods=['GET', 'POST'])
def add_contact():

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        conn = sqlite3.connect('contacts.db')
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO contacts(name, phone, email)
            VALUES (?, ?, ?)
            """,
            (name, phone, email)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('contacts'))

    return render_template('add_contact.html')


@app.route('/contact/<int:id>')
def contact_detail(id):

    conn = sqlite3.connect('contacts.db')
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM contacts WHERE id=?",
        (id,)
    )

    contact = cur.fetchone()

    conn.close()

    return render_template(
        'contact_detail.html',
        contact=contact
    )


@app.route('/delete/<int:id>')
def delete_contact(id):

    conn = sqlite3.connect('contacts.db')
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('contacts'))


if __name__ == '__main__':
    app.run(debug=True)