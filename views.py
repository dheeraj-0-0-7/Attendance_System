
@views.route("/")
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * from students')
    for db in cur:
        return db
    #return render_template("index.html")

@views.route("/login")
def login():
    return render_template("login.html")

@views.route("/register")
def register():
    return render_template("register.html")
