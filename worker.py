from flask import Flask
from flask import request
import requests
import os
import json
app = Flask(__name__)

def get_api_key() -> str:
    secret = os.environ.get("COMPUTE_API_KEY")
    if secret:
        return secret
    else:
        #local testing
        with open('.key') as f:
            return f.read()
      
@app.route("/")
def hello():
    return "Add workers to the Spark cluster with a POST request to add"

@app.route("/test")
def test():
    #return "Test" # testing 
    return(get_api_key())

@app.route("/add",methods=['GET','POST'])
def add():
  if request.method=='GET':
    return "Use post to add" # replace with form template~~
  else:
    token=get_api_key()
    ret = addWorker(token,request.form['num'])
    return ret


def addWorker(token, num):
    with open('payload.json') as p:
      tdata=json.load(p)
    tdata['name']='slave'+str(num)
    data=json.dumps(tdata)
    url='https://www.googleapis.com/compute/v1/projects/calcium-aria-371714/zones/europe-west1-b/instances'
    headers={"Authorization": "Bearer "+"ya29.a0AX9GBdW2I87MKeob3O8EBajgfTSmKXT8YkZ6JAfNPbbBHwjPSriyObMAQDwMi2eIsZ27zr9gpmudCDB-ZGKJOBKoZH_S_0t4wbppnZvUNcCl69tZAeswZh2O4C3Wr7zeRn3gRCLJznCMPAGO9bGAksrCKEiVNkzhlJKxTE2ATw3Q9Lk9cFELmfCdr3CeG8QSfs3FxFwzovIQrScVjXrD__mwqxhkJYoC85NZJOsaCgYKATASARMSFQHUCsbCiCLLcKCGl0j195eB3LNzgA0238"}
    resp=requests.post(url,headers=headers, data=data)
    if resp.status_code==200:     
      return "Done"
    else:
      print(resp.content)
      return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
