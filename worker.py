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
    headers={"Authorization": "Bearer "+ "ya29.a0AX9GBdWMkbq2W4cMN2wzx3lbKXI06LWADhmqB2lJx8y1g-zYDYnvOuXdhhFdPQaqyEmT0QyliWyORO_RtU0CQlfi58_wGriXBrB-fkiN59pg8j8E-bnQiQR1UL9_6N4AExm59OT7Fm-drA9JEYCv_ewbOJWc96-LQxz_F68E7I5LEU8fnjdCEySlWpcKqTxfItvcuN-K010lowEKA6n6HUbwEhAg0ccCG-mMKakaCgYKAaMSARMSFQHUCsbCVO0-jKFSc33u-9Pp2Q4gjQ0238"}
    resp=requests.post(url,headers=headers, data=data)
    if resp.status_code==200:     
      return "Done"
    else:
      print(resp.content)
      return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
