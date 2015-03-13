import os
from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse

import redis

app = Flask(__name__)
port = int(os.getenv("VCAP_APP_PORT"))

#db = redis.StrictRedis(host='localhost', port=6379, db=0)
api = restful.Api(app)

class Votes(restful.Resource):
    def post(self):
        #parser = reqparse.RequestParser()
        #parser.add_argument('vote', type=int)
        #args = parser.parse_args()
        #db.incrby('votes',args['vote'])
        #return db.get('votes').replace('"', '').strip() + " votes"
        return os.environ['VCAP_SERVICES']
    def get(self):
        return db.get('votes').replace('"', '').strip() + " votes"

api.add_resource(Votes, '/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
