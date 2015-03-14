import os
import json
from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse
import redis

app = Flask(__name__)
port = int(os.getenv("VCAP_APP_PORT"))
vcap = json.loads(os.environ['VCAP_SERVICES'])
svc = vcap['p-redis'][0]['credentials']

db = redis.StrictRedis(host=svc["host"], port=svc["port"], password=svc["password"],db=0)
api = restful.Api(app)

class Votes(restful.Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('vote', type=int)
        args = parser.parse_args()
        db.incrby('votes',args['vote'])
        return db.get('votes').replace('"', '').strip() + " votes"
    def get(self):
        if len(db.get('votes')) == 0:
            return "no votes"
        else:
            return db.get('votes').replace('"', '').strip() + " votes"


api.add_resource(Votes, '/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
