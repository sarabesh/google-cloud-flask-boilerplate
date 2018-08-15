from flask import Flask, render_template, request
import os
import MySQLdb
#from  flaskext.mysql import   MySQL
#import pymysql.cursors

#connection = pymysql.connect(host='127.0.0.1:3306',
#                             user='root',
#                             password='forgotpassword',
#                             db='db1',
#                             
#                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')



def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db
#mysql=MySQL()
#app.config['MYSQL_DATABASE_USER']='root'
#app.config['MYSQL_DATABASE_PASSWORD']='forgotpassword'
#app.config['MYSQL_DATABASE_DB']='db1'
#app.config['MYSQL_DATABASE_HOST']='127.0.0.1:3306'



@app.route('/')
def form():
    return render_template('form.html')
@app.route('/submitted_form', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']
    #conn=mysql.connect()
    #cursor=conn.cursor()
    #check_stmt=("SELECT * FROM table1 ")
    #check_data=(clg)
    #cursor.execute(check_stmt,check_data)
    #data=cursor.fetchall()
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print "Database version : %s " % data
    print("start")
    cursor.execute("INSERT into table1 VALUES ('sarabesh','sffg@se.com','dag.com','srh',5)")
    db.commit()
    sql = "INSERT INTO table1 VALUES ('%s', '%s', '%s', '%s', '%d' )" % (name,email,site,comments, 2000)
    try:
        cursor.execute(sql)
        print("success")
        cond='success'
        db.commit()
    except:
        print("failure")
        cond='failure'
        db.rollback()
    db.close()
    # cursor = db.cursor()
    # cursor.execute('SELECT * from table1')
    # for r in cursor.fetchall():
    #     self.response.write('{}\n'.format(r))

    return render_template(
    'submitted_form.html',
    name=name,
    email=email,
    site=site,
    comments=comments,
    cond=cond,
    data=data)