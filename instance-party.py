import os
import json
import threading
import time
from time import sleep
from flask import Flask, json, render_template, request
import redis

app = Flask(__name__)
port = int(os.getenv("PORT"))
vcap = json.loads(os.environ['VCAP_SERVICES'])
svc = vcap['rediscloud'][0]['credentials']

db = redis.StrictRedis(host=svc["hostname"], port=svc["port"], password=svc["password"],db=0)

def heartbeat():
    while True:
        instance_id = os.getenv("CF_INSTANCE_INDEX")
        db.hset("party",instance_id,time.time())
        sleep(0.5)

@app.route('/register')
def register():
    mydict = db.hgetall("party")
    mylist = []
    for k in mydict:
        if float(mydict[k]) > (time.time() - 1):
            mylist.append(k)
    return render_template('robots.html', mylist=mylist)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    t = threading.Thread(target=heartbeat)
    t.start()
    app.run(host='0.0.0.0', port=port, debug=True)
