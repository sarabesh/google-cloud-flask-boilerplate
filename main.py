import os
from flask import Flask, render_template, request
import MySQLdb


app = Flask(__name__)
# These environment variables are configured in app.yaml.
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
    
@app.route('/')
def Home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/items')
def items():
    db=connect_to_cloudsql()
    cursor=db.cursor()
    cursor.execute('use db1')
    cursor.execute('SELECT * FROM products')
    k=cursor.fetchall()
    db.close()

    return render_template('items.html',**locals())



@app.route('/form')
def form():
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute('use db1')
    cursor.execute('SELECT * FROM table1')
    k=cursor.fetchall()
    db.close()
    
    return render_template('form.html',**locals()) 

@app.route('/submitted_form', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute('use db1')
    sql = """INSERT INTO table1  VALUES ('hi', 'test', 'now', 'not', 288)"""
    cursor.execute('DESC table1')
    k=cursor.fetchall()
    cursor.execute(sql)
    
    db.commit()
    db.close()
   

    return render_template('submitted_form.html',**locals())
 






if __name__ == '__main__':
    app.run()  