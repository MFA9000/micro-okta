from flask import Flask, render_template,request,session,jsonify,redirect,url_for
from flask_session import Session
import requests
import json
import helper_function as okta
from flask_cors import CORS

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)

# To run python file without re-running the flask command
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)


# Routes
@app.route('/')
def home():
    return "Okta-Microservice"


@app.route('/login')
def login():
    username = request.args.get('id')
    password = request.args.get('pass')
    flag,session_token=okta.Session_token(username,password)
    if flag:
        session["user"]=username
        session["session_token"]=session_token
        okta.Send_OTP(username)
        print(session['domain']+'/login_callback')
        return redirect(session['domain']+'/login_callback')
    return redirect(session['domain']+'/login')

@app.route('/verify-otp')	
def otp():
    username = session["user"]
    pin= request.args.get('pin')
    if okta.Verify_OTP(username,pin):
        print('1')
        session_token = session["session_token"]
        flag,data=okta.Create_Session(session_token)
        if flag:
            print('2')
            session["session_id"]=data[0]
            session["user_id"]=data[1]   
            print(session['callback'])
            return redirect(session['callback'])
    session["session_token"]=''
    return redirect(session['domain']+'/login')
   
   	
@app.route('/Auth')
def Auth():
    callback = request.args.get('callback')
    domain = okta.extract(callback)
    session['callback']=callback
    session['domain']=domain
    try:
        session_id=session["session_id"]
        if okta.Validate_Session(session_id):
            return redirect(session['callback']+'?session_id='+session_id)
        else:
            return redirect(session['domain']+'/login')
    except:
        return redirect(session['domain']+'/login')


@app.route('/validate')
def validate():
    session_id = request.args.get('session_id')
    if okta.Validate_Session(session_id):
        return jsonify({'key':1})
    else:
        return jsonify({'key':0})

        
@app.route('/logout')
def Logout():
    session['user']=''
    session['session_token']=''
    session['session_id']=''
    session['user_id']=''
    return redirect(session['callback'])
    

# init
if __name__ == '__main__':
    app.run(debug=True)

