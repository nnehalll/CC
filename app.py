from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'bdf98aaba1e90e5b5a28fa44d2b03d3b'

# Storage for users (username: {email, password, full_name})
users = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        if username in users:
            flash("Username already exists!")
            return redirect(url_for('register'))

        users[username] = {'email': email, 'password': password, 'full_name': full_name}
        flash("Registration successful!")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            flash("Login successful!")
            return redirect(url_for('welcome'))

        flash("Invalid username or password!")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        username = session['username']
        full_name = users[username]['full_name']
        return render_template('welcome.html', full_name=full_name)
    else:
        flash("Please log in to view this page.")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)