import requests
import json
org="dev-36276890.okta.com"
api="00Ess0k505JrLe_vDuuXpDsDb1zUHMwAii6JE4LSMW"

def Session_token(username,password):
    raw='{"username":"%s","password":"%s", "options": {"multiOptionalFactorEnroll": true,"warnBeforePasswordExpired": true}}'
    raw=raw%(username,password)
    header = {'Accept' : 'application/json' , 'Content-Type' : 'application/json'}
    re=requests.post("https://%s/api/v1/authn"%(org), data=raw, headers=header)
    re=json.loads(re.text)
    try:
        re["status"]
        return True,re['sessionToken']
       
    except:
        return False,''
    
def User_id(username):
    raw="https://%s/api/v1/users?q=%s"%(org,username)
    header = {'Accept' : 'application/json' , 'Content-Type' : 'application/json', 'Authorization' : 'SSWS %s'%(api)}
    re=requests.get(raw,headers=header)
    re=json.loads(re.text)
    return re[0]['id']
    
def Fact_id(User_id):
    raw="https://%s/api/v1/users/%s/factors"%(org,User_id)
    header = {'Accept' : 'application/json' , 'Content-Type' : 'application/json', 'Authorization' : 'SSWS %s'%(api)}
    re=requests.get(raw,headers=header)
    re=json.loads(re.text)
    return re[0]['id']
    
def Send_OTP(username):
    User=User_id(username)
    Factor=Fact_id(User)
    raw="https://%s/api/v1/users/%s/factors/%s/verify"%(org,User,Factor)
    header = {'Accept' : 'application/json' , 'Content-Type' : 'application/json', 'Authorization' : 'SSWS %s'%(api)}
    requests.post(raw,headers=header)
 
def Verify_OTP(username,pin):
    User=User_id(username)
    Factor=Fact_id(User)
    otp='{"passCode": "%s"}'%(pin)  
    raw="https://%s/api/v1/users/%s/factors/%s/verify"%(org,User,Factor)
    header = {'Accept' : 'application/json' , 'Content-Type' : 'application/json', 'Authorization' : 'SSWS %s'%(api)}
    re=requests.post(raw,headers=header,data=otp)
    re=json.loads(re.text)
    try:
        re["factorResult"]
        return True
    except:
        return False
        
def Create_Session(s_token):
    raw='https://%s/api/v1/sessions?additionalFields=cookieToken'%(org)
    header = {'Accept' : 'application/json' , 'Content-Type' : 'application/json', 'Authorization' : 'SSWS %s'%(api)}
    token='{"sessionToken": "%s"}'%(s_token)
    re=requests.post(raw,headers=header,data=token)
    re=json.loads(re.text)
    try:
        session_id=re['id']
        user_id=re['userId']
        return True,[session_id,user_id]
    except:
        return False,[]

def Validate_Session(session_id):
    raw='https://%s/api/v1/sessions/%s'%(org,session_id)
    header = {'Accept' : 'application/json' , 'Content-Type' : 'application/json', 'Authorization' : 'SSWS %s'%(api)}
    re=requests.get(raw,headers=header)
    re=json.loads(re.text)
    if re["status"]=="ACTIVE":
        return True
    else:
        return False
        
def info(session_id):
    raw='https://%s/api/v1/sessions/%s'%(org,session_id)
    header = {'Accept' : 'application/json' , 'Content-Type' : 'application/json', 'Authorization' : 'SSWS %s'%(api)}
    re=requests.get(raw,headers=header)
    re=json.loads(re.text)
    return re

def name(session_id):
    raw='https://%s/api/v1/sessions/%s'%(org,session_id)
    header = {'Accept' : 'application/json' , 'Content-Type' : 'application/json', 'Authorization' : 'SSWS %s'%(api)}
    re=requests.get(raw,headers=header)
    re=json.loads(re.text)
    return re["_links"]["user"]["name"]
        
def extract(callback):
    inst= callback.split('/')
    return inst[0]+'//'+inst[2]
