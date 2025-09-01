#Import necessary libraries
from flask import Flask, request, render_template, redirect, url_for, session
import hashlib
import redis
import os

#Initialize Flask app
app = Flask(__name__)
#Set a secret key for session management, retrieved from environment variables
app.secret_key = os.getenv('SECRET_KEY')

#Connect to Redis database
r = redis.Redis(host='redis-db', port=6379, db=0, decode_responses=True)

def hash_password(password):
    #Convert password to SHA-256 hash for secure storage
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    #Handle user registration
    data = request.form
    username = data.get('username', '')
    email = data.get('email', '')
    password = data.get('password', '')
    repeat_email = data.get('repeat_email', '')

    #Validate that all fields are filled
    if not username or not email or not password or not repeat_email:
        return render_template('main.html.j2', message='All fields are required.')

    #Check if the email seems valid (simple check without regex for demonstration)
    if '@' not in email or '.' not in email:
        return render_template('main.html.j2', message='Please enter a valid email address.')

    #Check if passwords match
    if email != repeat_email:
        return render_template('main.html.j2', message='Emails do not match.')

    #Check if username or email already exists
    if r.hexists(f"user:{username}", 'email') or r.sismember('emails', email):
        return render_template('main.html.j2', message='Username or email already exists.')

    #Save new user data in Redis
    user_key = f"user:{username}"
    r.hset(user_key, mapping={'email': email, 'password': hash_password(password)})
    r.sadd('emails', email)  #Add email to set of emails

    #Redirect to login page with success message
    return redirect(url_for('login', message='User registered successfully'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    #POST: Process login form submission
    if request.method == 'POST':
        #Extract username and password from submitted form data
        data = request.form
        username = data['username']
        password = data['password']
        
        #Use username to fetch associated user data from Redis
        user_key = f"user:{username}"
        user_data = r.hgetall(user_key)

        #Verify user exists and check password validity
        if user_data:
            stored_password_hash = user_data.get('password')
            if hash_password(password) == stored_password_hash:
                #Password correct: Establish user session and redirect to home page
                session['username'] = username
                return redirect('http://localhost:85/home')
            else:
                #Password incorrect: Set error message
                message = 'Invalid password'
        else:
            #Username not found: Set error message
            message = 'Invalid username'
            
        #Login failed: Re-render login form with error message
        return render_template('main.html.j2', message=message)

    #GET: Show login form (with optional message, e.g., after registration)
    else:
        message = request.args.get('message', '')
        return render_template('main.html.j2', message=message)


@app.route('/logout')
def logout():
    #Log out user by removing from session
    session.pop('username', None)
    return redirect('http://localhost:85/login')

#Run the app in development mode on port 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


