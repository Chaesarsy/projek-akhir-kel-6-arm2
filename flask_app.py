
# A very simple Flask Hello World app for you to get started with...

import random
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import json
import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_monitoring'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                print(user['status'])
                if user['status'] == 0:
                    flash("user not activated!")
                    return redirect(url_for('login'))
                else:
                    if user['role'] == 'admin' :
                        session['role'] = user['role']
                        session['name'] = user['name']
                        session['email'] = user['email']
                        isMobile = request.args.get('mobile')
                        if isMobile == "true":
                            return json.dumps({'email': user['email'], 'role': user['role']})
                        else:
                            return render_template("home.html")
                    else :
                        session['name'] = user['name']
                        session['email'] = user['email']
                        isMobile = request.args.get('mobile')
                        if isMobile == "true":
                            return json.dumps({'email': user['email'], 'role': user['role']})
                        else:
                            return render_template("home.html")
            else:
                isMobile = request.args.get('mobile')
                if isMobile == "true":
                    return "json.dumps({'email': user['email'], 'role': user['role']})"
                else:
                    flash("Error: password and email not match")
                    return redirect(url_for('login'))

        else:
            isMobile = request.args.get('mobile')
            if isMobile == "true":
                return "json.dumps({'email': user['email'], 'role': user['role']})"
            else:
                flash("Error: user not found")
                return redirect(url_for('login'))
    else:
        return render_template("login.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
     return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, role, status) VALUES (%s,%s,%s, %s,0)",
                    (name, email, hash_password, 'user'))
        mysql.connection.commit()
        flash("registrasi anda berhasil!   Silahkan Login...")
        return redirect(url_for('login'))

@app.route('/ban')
def ban():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ban")
    rv = cur.fetchall()
    cur.close()
    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return json.dumps(rv)
    else:
        return render_template('ban.html', bans=rv)


@app.route('/insert-ban', methods=["POST"])
def insertBanWeb():
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    start = datetime.datetime.strptime(startDate, "%m/%d/%Y %I:%M %p")
    end = datetime.datetime.strptime(endDate, "%m/%d/%Y %I:%M %p")
    deltaTgl = end - start
    insertBan(deltaTgl.days + 1, start, end)
    return redirect(url_for('ban'))

@app.route('/insert-ban-mobile', methods=["POST"])
def insertBanMobile():
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    start = datetime.datetime.strptime(startDate, "%d/%m/%Y")
    end = datetime.datetime.strptime(endDate, "%d/%m/%Y")
    deltaTgl = end - start
    insertBan(deltaTgl.days + 1, start, end)
    return "success"

def insertBan(iterations, start, end):
    cur = mysql.connection.cursor()

    Delete_all_rows = """truncate table ban """
    cur.execute(Delete_all_rows)
    mysql.connection.commit()

    for x in range(iterations):
        target = random.randint(1, 6)
        aktual = random.randint(1, 10)
        status = ''

        if aktual < target:
            status = 'under performance'
        elif aktual > target :
            status ='performance'
        else :
            status = 'on target'

        date = start + datetime.timedelta(days=x)
        tanggal = date.strftime("%d/%m/%Y")

        cur.execute("INSERT INTO ban (tanggal, target, aktual, status) VALUES (%s, %s, %s, %s)", (tanggal, target, aktual, status))
        mysql.connection.commit()
    return "success"

@app.route('/velg')
def velg():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM velg")
    rv = cur.fetchall()
    cur.close()
    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return json.dumps(rv)
    else:
        return render_template('velg.html', velgs=rv)

@app.route('/insert-velg', methods=["POST"])
def insertVelgWeb():
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    start = datetime.datetime.strptime(startDate, "%m/%d/%Y %I:%M %p")
    end = datetime.datetime.strptime(endDate, "%m/%d/%Y %I:%M %p")
    deltaTgl = end - start
    insertVelg(deltaTgl.days + 1, start, end)
    return redirect(url_for('velg'))

@app.route('/insert-velg-mobile', methods=["POST"])
def insertVelgMobile():
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    start = datetime.datetime.strptime(startDate, "%d/%m/%Y")
    end = datetime.datetime.strptime(endDate, "%d/%m/%Y")
    deltaTgl = end - start
    insertVelg(deltaTgl.days + 1, start, end)
    return "success"

def insertVelg(iterations, start, end):
    cur = mysql.connection.cursor()

    Delete_all_rows = """truncate table velg """
    cur.execute(Delete_all_rows)
    mysql.connection.commit()

    for x in range(iterations):
        target = random.randint(1, 6)
        aktual = random.randint(1, 10)
        status = ''

        if aktual < target:
            status = 'under performance'
        elif aktual > target :
            status ='performance'
        else :
            status = 'on target'

        date = start + datetime.timedelta(days=x)
        tanggal = date.strftime("%d/%m/%Y")

        cur.execute("INSERT INTO velg (tanggal, target, aktual, status) VALUES (%s, %s, %s, %s)", (tanggal, target, aktual, status))
        mysql.connection.commit()
    return "success"

@app.route('/update-user', methods=["POST"])
def updateUser():
    id_data = request.form['id']
    email = request.form['email']
    name = request.form['nama']
    status = request.form['status']
    role = request.form['role']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET email=%s, name=%s, status=%s, role=%s WHERE Id=%s", (email, name, status, role, id_data,))
    mysql.connection.commit()
    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return "success"
    else:
        return redirect(url_for('admin'))

@app.route('/admin', methods=["GET"])
def admin():
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT * FROM users")
    rv = curl.fetchall()
    curl.close()
    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return json.dumps(rv)
    else:
        return render_template("admin.html", users=rv)

@app.route('/about-us')
def AboutUs():
    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return "json succes" #json.dumps(users)
    else:
        return render_template("about-us.html")

if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(host="0.0.0.0", port=5000, debug=True)
