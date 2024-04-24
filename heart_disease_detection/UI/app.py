
from flask import Flask, render_template, request, session, url_for, redirect,jsonify
from werkzeug.utils import secure_filename
import os
# from flask import Flask, render_template, request
import pickle
import pymysql
import pandas as pd
import json
import datetime
# import tensorflow
# from tensorflow import keras
# from tensorflow.keras.models import load_model


import tensorflow as tf
tf.config.experimental.list_physical_devices('GPU')
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    # Restrict TensorFlow to only allocate 1GB * 2 of memory on the first GPU
    try:
        tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024 * 4)])
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Virtual devices must be set before GPUs have been initialized
        print(e)

app = Flask(__name__)

def dbConnection():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="root", database="object_detect",charset='utf8' ,port=3306)
        return connection
    except:
        print("Something went wrong in database Connection")

def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")

con=dbConnection()
cursor=con.cursor()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'random string'

##########################################################################################################
#                                           Register
##########################################################################################################
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        # print("hii register")
        email = request.form['Email']
        password = request.form['pass1']
        username = request.form['Name']

        print(email,password,username)

        try: 
            con = dbConnection()
            cursor = con.cursor()
            sql1 = "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
            val1 = (username, email, password)
            cursor.execute(sql1, val1)
            print("query 1 submitted")
            con.commit()

            FinalMsg = "Congrats! Your account registerd successfully!"
        except:
            con.rollback()
            msg = "Database Error occured"
            print(msg)
            return render_template("login.html", error=msg)
        finally:
            dbClose()
        return render_template("login.html",FinalMsg=FinalMsg)
    return render_template("register.html")
##########################################################################################################
#                                               Login
##########################################################################################################
@app.route("/", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password'] 

        print(email,password)

        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password))
        result = cursor.fetchone()
        print("result")
        print(result)
        if result_count>0:
            print("len of result")
            session['uname'] = result[1]
            session['userid'] = result[0]
            return redirect(url_for('root'))
        else:
            return render_template('login.html')
    return render_template('login.html')
##########################################################################################################
#                                       Prediction
##########################################################################################################
# import cv2
# import numpy as np
# import serial
# import time



@app.route("/single", methods = ['POST', 'GET'])
def single():
    username=session.get('uname')
    print(username)
    if request.method=="POST":
        print("hgjgh")

        # details = request.form
        
        fname = request.form['fname']
        Age = request.form['Age']
        sex = request.form['option']
       
        trestbps = request.form['trestbps']
        chol = request.form['chol']
        print(trestbps)
        
        pain = request.form['option1']
        thalach = request.form['thalach']
        sugarlevel = request.form['option2']
        slope = request.form['slope']
        ca = request.form['ca']
        exercise = request.form['option3']
        
       
        print(Age)
        print("user_inp")
        print(fname,Age,sex,trestbps,chol,pain,thalach,sugarlevel,slope,ca,exercise)
        print()
       

        userdict = {
            "age":Age,
            "sex":sex,
            "trestbps":trestbps,
            "chol":chol,
            "cp":pain,
            "thalach":thalach,
            "fbs":sugarlevel,
            "slope":slope,
            "ca":ca,
            "exang":exercise
        }
        
        df = pd.DataFrame(userdict, index=[0])
        print(df)

        with open('RandomForest_pickle', 'rb') as f:
            rfc_users = pickle.load(f)

        predicted_op = rfc_users.predict(df)
        predicted_value = str(predicted_op[0])
        print("===========================")
        print()
        print(predicted_value)
 
        print(type(predicted_value))
        print()
        print("===========================")

        if( predicted_value=="0"):
            final_prediction = "Normal"
            print("========================================")
            print(final_prediction)
            print("========================================")
        
            response_data = {
                    'response_1': final_prediction,
                    'response_2': fname
                }
            return jsonify(response_data)
        
              
        elif(predicted_value=="1"):
            final_prediction = "Fixed Defect"
            print("========================================")
            print(final_prediction)
            print("========================================")
         
            response_data = {
                    'response_1': final_prediction,
                    'response_2': fname
                }
            return jsonify(response_data)
        
        elif(predicted_value=="2"):
            final_prediction = "Reversable Defect"
            print("========================================")
            print(final_prediction)
            print("========================================")
         
            response_data = {
                    'response_1': final_prediction,
                    'response_2': fname
                }
            return jsonify(response_data)
        
        else:
            final_prediction = "slightly Defect"
            print("========================================")
            print(final_prediction)
            print("========================================")
         
            response_data = {
                    'response_1': final_prediction,
                    'response_2': fname
                }
            return jsonify(response_data)
            
            

        # return render_template('services.html',final_prediction=final_prediction)
    return render_template('services.html')

##########################################################################################################
#                                               getfetch
##########################################################################################################
@app.route('/fetch_data', methods=['POST'])
def fetch_data():
   
    data = request.get_json()
    final_prediction = data.get('value')
    print(final_prediction)
    con = dbConnection()
    cursor = con.cursor()
    result_count = cursor.execute('SELECT * FROM classification WHERE Disease = %s', (final_prediction,))
    result = cursor.fetchone()
    print(result)
    # Convert the result to JSON
    result_json = json.dumps(result)
    
    return jsonify({'result': result_json})




##########################################################################################################
#                                               about
##########################################################################################################
@app.route("/about", methods = ['POST', 'GET'])
def about():
    
    return render_template('about.html')
##########################################################################################################
#                                               contact
##########################################################################################################
@app.route("/contact", methods = ['POST', 'GET'])
def contact():
    username=session.get('uname')
    if request.method=="POST":
        user_name = request.form.get("Name")
        user_email = request.form.get("Email")
        user_test = request.form.get("test")
        user_massage = request.form.get("Message")
        uploadimg = request.files['file']
        current_datetime = datetime.datetime.now()
        
        filename_secure = secure_filename(uploadimg.filename)
        uploadimg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_secure))
        filenamepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_secure)
        
        con = dbConnection()
        cursor = con.cursor()
        sql1 = "INSERT INTO contact(session, user_name, user_email, user_test, user_massage,current_datetime,uploadimg) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val1 = (username, user_name, user_email, user_test, user_massage, current_datetime, filenamepath)
        cursor.execute(sql1, val1)
        print("query 1 submitted")
        con.commit()
        FinalMsg = "Congrats! Your request  registerd successfully!"
        return FinalMsg
      
    return render_template('contact.html',firstName=username)
##########################################################################################################
#                                               contact
##########################################################################################################
@app.route("/logout", methods = ['POST', 'GET'])
def logout():
    session.pop('uname',None)
    session.pop('userid',None)
    return redirect(url_for('login'))
#########################################################################################################
#                                       Home page
##########################################################################################################
@app.route("/root")
def root():
    if 'uname' in session:
        username=session.get('uname')
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM contact')
        result = cursor.fetchall()
        print("result")
        # print(result)
        
        return render_template('index.html',result=result)


if __name__=='__main__':
    # app.run(debug=True)
    app.run('0.0.0.0')