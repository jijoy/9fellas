import os
import json
from flask import Flask, json, render_template, request
import redis

app = Flask(__name__)
port = int(os.getenv("VCAP_APP_PORT"))
vcap = json.loads(os.environ['VCAP_SERVICES'])
svc = vcap['rediscloud'][0]['credentials']

db = redis.StrictRedis(host=svc["hostname"], port=svc["port"], password=svc["password"],db=0)

@app.route('/register')
def register():
    instance_id = os.getenv("CF_INSTANCE_INDEX")
    db.sadd("instances",(instance_id))
    mylist = db.smembers("instances")
    return render_template('robots.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
