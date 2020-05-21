import sqlite3
from flask import Flask, render_template, request, config

app = Flask(__name__)


def connect_db():
    return sqlite3.connect(config.DATABASE_NAME)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/SIGN-IN")
def signin():
    return render_template('login.html')


@app.route("/SIGN-UP")
def signup():
    return render_template("signup.html")


@app.route("/success")
def success():
    return render_template('success.html')


@app.route("/signsuccess")
def signsuccess():
    return render_template('signsuccess.html')


@app.route('/LOGIN', methods=['POST', 'GET'])
def LOGIN():
    if request.method == 'POST':
        try:
            userid = request.form['ID']
            user_name = request.form['Name']
            password = request.form['Password']
            mobile_no = request.form['Phone']
            with sqlite3.connect('binpy.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO signup(userid,user_name,password,mobile_no) VALUES (?,?,?,?)",
                            (userid, user_name, password, mobile_no))
                con.commit()
                msg = "record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("success.html", msg=msg)
            con.close()


@app.route('/LOGIN1', methods=['POST', 'GET'])
def LOGIN1():
    if request.method == 'POST':
        try:
            userid = request.form['userid']
            password = request.form['password']
            with sqlite3.connect('binpy.db') as con:
                cur = con.cursor()
                found = 0
                for row in cur.execute("SELECT userid, password from login"):
                    id = row[0]
                    pwd = row[1]
                    if id == userid and pwd == password:
                        msg = "Logged in"
                        found = 1
                        break
                if found == 0:
                    msg = "Try again"

        except:
            con.rollback()
            msg = "error"
        finally:
            return render_template("signsuccess.html", msg=msg)
            con.close()


if __name__ == "__main__":
    app.run()
