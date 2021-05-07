from flask import Flask, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
import json
import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'kelompok6'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        status = request.form['status']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                if request.form['status'] == user["status"]:
                    return render_template("home.html")
                else: 
                    return "Akun anda belum terverifikasi"
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
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
        posisi = request.form['select']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, posisi) VALUES (%s,%s,%s,%s)",
        (name, email, hash_password, posisi))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))

@app.route('/velg')
def velg():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM velg")
    rv = cur.fetchall()
    cur.close()
    return render_template('velg.html', velgs=rv)

@app.route('/insert-velg', methods=["POST"])
def insertVelg():
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    start = datetime.datetime.strptime(startDate, "%d/%m/%Y")
    end = datetime.datetime.strptime(endDate, "%d/%m/%Y")
    deltaTgl = end - start

    cur = mysql.connection.cursor()

    Delete_all_rows = """truncate table velg """
    cur.execute(Delete_all_rows)
    mysql.connection.commit()

    for x in range(deltaTgl.days + 1):
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
        print (tanggal)
        cur.execute("INSERT INTO velg (tanggal, target, aktual, status) VALUES (%s, %s, %s, %s)", (tanggal, target, aktual, status))
        mysql.connection.commit()

    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return "success"
    else:
        return 'success html'#redirect(url_for('dummypart'))
        
@app.route('/ban')
def ban():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ban")
    rv = cur.fetchall()
    cur.close()
    return render_template('ban.html', bans=rv)

@app.route('/insert-ban', methods=["POST"])
def insertban():
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    start = datetime.datetime.strptime(startDate, "%d/%m/%Y")
    end = datetime.datetime.strptime(endDate, "%d/%m/%Y")
    deltaTgl = end - start

    cur = mysql.connection.cursor()

    Delete_all_rows = """truncate table ban """
    cur.execute(Delete_all_rows)
    mysql.connection.commit()

    for x in range(deltaTgl.days + 1):
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

    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return "success"
    else:
        return 'success html'#redirect(url_for('dummypart'))

@app.route('/control')
def control():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM control")
    rv = cur.fetchall()
    cur.close()
    return render_template('control.html', controls=rv)

#@app.route('/simpan-control', methods=["POST"])
#def saveControl():
 #   tanggal = request.form['tanggal']
  #  jumlahproduksibusi = request.form['jumlah produksi busi']
 #   targetproduksibusi = request.form['target produksi busi']
  #  jumlahproduksiaki = request.form['jumlah produksi aki']
 #   targetproduksiaki = request.form['target produksi aki']
 #   cur = mysql.connection.cursor()
 #   cur.execute("INSERT INTO control (tanggal, jumlah produksi busi, target produksi busi, jumlah produksi aki, target produksi aki) VALUES (%s, %s, %s, %s, %s)", (tanggal, jumlahproduksibusi, targetproduksibusi, jumlahproduksiaki, targetproduksiaki))
 #   mysql.connection.commit()
 #   return redirect(url_for('control'))

@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    rv = cur.fetchall()
    cur.close()
    return render_template('admin.html', admins=rv)
    
@app.route('/apply', methods=["POST"])
def apply():
    id_users = request.form['id']
    status = request.form['apply']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET status=%s WHERE id=%s", (status, id_users))
    mysql.connection.commit()
    return redirect(url_for('admin'))

@app.route('/about-us')
def about():
    return render_template("about-us.html")


if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True) 