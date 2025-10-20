# proj_name = get_project()
# dbname = proj_name['animal_adoption']
# animals_collection = dbname['animals']
# users_collection = dbname['users']

# user1 = {
#     "admin_access": False,
#     "first_name": 'Michael',
#     "last_name": 'Scott',
#     "email": 'mscott@gmail.com',
#     "password": 'Dunder Mifflin',
# }

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        #is the following correct with Flask-WTF?
        entered_login = {'email': email, 'password': password}
        if users_collection.find_one(entered_login):
            flash("Log in successful.")
            return render_template('index.html')
        else:
            flash("User not found. Please try again or create an account.")
            return redirect('/login')
    return render_template('login.html')
        
   
    
@app.route('/register', methods=['GET', 'POST'])
def createUser():
    form = RegisterForm()
    if form.validate_on_submit():
        admin_access = form.admin_access.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        #is the following correct with Flask-WTF?
        user = {"admin_access": admin_access, "first_name": first_name, "last_name": last_name, "email": email, "password": password}
        if users_collection.find_one(user):
            flash("User already exists.")
            return render_template('register.html')
        else:
            users_collection.insert_one(user)
            flash("User created successfully. Please log in.")
            return render_template('login.html')
    return render_template('register.html')