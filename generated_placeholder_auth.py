
# Generated with help from Gemini

import psycopg2

DATABASE_URL = "your_database_url"

def insert_user(email, password):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        query = "INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id, email, user_type, tokens;"
        cur.execute(query, (email, password))
        new_user = cur.fetchone()
        conn.commit()
        return new_user
    except (Exception, psycopg2.Error) as error:
        print(f"Error while inserting user: {error}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            cur.close()
            conn.close()

# Example usage:
new_user = insert_user("test@example.com", "securepassword")
if new_user:
    print(f"New user created with ID: {new_user[0]}")



######################################

from flask import Flask, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # IMPORTANT for session security in a real app

# Assume a simplified way to "identify" a user for the demo
users_data = {
    'free_user': {'id': 'some_free_id', 'email': 'free@example.com', 'user_type': 'FREE'},
    'paid_user': {'id': 'some_paid_id', 'email': 'paid@example.com', 'user_type': 'PAID'},
    'super_user': {'id': 'some_super_id', 'email': 'super@example.com', 'user_type': 'SUPER'},
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = users_data.get(username)
        if user:
            session['user_id'] = user['id']
            session['user_type'] = user['user_type']
            return redirect(url_for('home'))
        else:
            return 'Login failed'
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username">
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/')
def home():
    user_type = session.get('user_type')
    if user_type == 'FREE':
        return 'Welcome, Free User!'
    elif user_type == 'PAID':
        return 'Welcome, Paid User! You have access to premium features.'
    elif user_type == 'SUPER':
        return 'Welcome, Super User! You have all privileges.'
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


######################################
