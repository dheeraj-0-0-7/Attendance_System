from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'aws-0-us-east-1.pooler.supabase.com'
app.config['MYSQL_USER'] = 'postgres.wfndeugctludkryndzme'
app.config['MYSQL_PASSWORD'] = 'dbforstudentsattendance'
app.config['MYSQL_DB'] = 'postgres'

mysql = MySQL(app)

cur = mysql.connection.cursor()
cur.execute('SELECT * from students')
