import base64
import os
import sqlite3

import cv2
import numpy as np
import sys
from flask import Flask, render_template, request, config, flash
import tensorflow as tf
import re
import cv2
import numpy as np
import pytesseract
from PIL import Image

src_path = "/home/anagha/Desktop/uploads/"

from keras.preprocessing import image
from keras_applications.imagenet_utils import decode_predictions, preprocess_input
from keras_preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import Sequential
from werkzeug.utils import secure_filename, redirect

sys.path.append(os.path.abspath("./model"))


def init():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = tf.keras.models.model_from_json(loaded_model_json)
    loaded_model.load_weights("model.h5")
    print("loaded model from disk")

    loaded_model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']

    )
    # graph = tf.get_default_graph()
    tf.compat.v1.disable_eager_execution()

    gr = tf.compat.v1.get_default_graph()
    return loaded_model, gr


UPLOAD_FOLDER = '/home/anagha/PycharmProjects/Bin-py/uploads'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

global model, graph
model, graph = init()
print("successful")


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


@app.route("/UPLOAD")
def upload():
    return render_template('upload.html')


def processImg(filename):
    image = load_img(UPLOAD_FOLDER + filename, target_size=(300, 300))
    image = img_to_array(image)
    image = np.array(image)
    res = model.predict(image)
    i = 0
    ind = 0
    large = res[0][0]
    for k in res[0]:
        if k > large:
            large = k
            i = ind
        ind += 1
    res_ind = i
    return res_ind


UPLOAD_FOLDER = '/home/anagha/Desktop/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



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
    print('inside login')
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

src_pathc = "/home/anagha/Desktop/uploads/cardboard2.jpg"
print(src_pathc)


@app.route('/PREDICT', methods=['POST', 'GET'])
def PREDICT():
        
    if request.method == 'POST':
     

        image = request.files['image']
        print(image.filename)
        print(image)
        return redirect(request.url)

        print('savedimage')
        if image:
            passed = False
            try:
                filename = image.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print("saved")
                image.save(filepath)
                passed = True
                print(passed)
            except Exception:
                passed = False

        print(passed)
        resp = processImg('file.filename')

        print(resp)
        if resp == 0:
            return render_template('cardboard.html')
        if resp == 1:
            return render_template('glass.html.html')
        if resp == 2:
            return render_template('paper.html')
        if resp == 3:
            return render_template('metal.html')
        if resp == 4:
            return render_template('plastic.html')
        return None
    else:
        print('else')


    



if __name__ == "__main__":
    app.run()
