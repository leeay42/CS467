
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get login information from user
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        entered_login = {'email': email, 'password': password}
        user = users_collection.find_one(entered_login)
        # Check database for login credentials
        if user:
            session['admin_access'] = user.get('admin_access')
            flash("Log in successful.")
            return render_template('index.html')
        else:
            flash("User not found. Please try again or create an account.")
            return redirect('/login')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def createUser():
    # Get account information from user
    form = RegisterForm()
    if form.validate_on_submit():
        admin_access = form.admin_access.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        user = {"admin_access": admin_access, "first_name": first_name, "last_name": last_name, "email": email, "password": password}
        # Check that user info doesn't already exist in DB
        if users_collection.find_one(user):
            flash("User already exists. Please try again.")
            return render_template('register.html')
        # Create user account in DB
        else:
            users_collection.insert_one(user)
            flash("User created successfully. Please log in.")
            return render_template('login.html')
    return render_template('register.html')