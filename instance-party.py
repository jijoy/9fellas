import os
import json
from threading import Thread
import time
from time import sleep
from flask import Flask, json, render_template, request
import redis

from Queue import Queue

app = Flask(__name__)
port = int(os.getenv("PORT"))
vcap = json.loads(os.environ['VCAP_SERVICES'])
svc = vcap['rediscloud'][0]['credentials']

db = redis.StrictRedis(host=svc["hostname"], port=svc["port"], password=svc["password"],db=0)



class Producer(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue 
    def run(self):
        while True :
            try:
                instance_id = os.getenv("CF_INSTANCE_INDEX")
                mydict = db.hgetall("party")
                if instance_id not in mydict :
                    self.queue.put(instance_id)
            except :
                pass
            finally:
                pass
class Consumer(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        while True :
            try :
                instance_id = self.queue.get()
                db.hset("party",instance_id,1)
            except:
                pass
            finally:
                pass
            
# def heartbeat():
#     while True:
#         instance_id = os.getenv("CF_INSTANCE_INDEX")
#         db.hset("party",instance_id,time.time())
#         sleep(0.5)
        
def init_workers():
    party_queue = Queue()
    p = Producer(party_queue)
    p.daemon = True
    c = Consumer(party_queue)
    c.deamon= True
    p.start()
    c.start()

@app.route('/addthread')
def addthread():
    instance_id = os.getenv("CF_INSTANCE_INDEX")
    print 'Instance Id ****************%s'%instance_id
    thread_count = int(db.hget("party",instance_id))
    thread_count+=1
    print 'Threadcount ****************%s'%thread_count
    result = db.hset("party",str(instance_id),str(thread_count))
    print 'HSET result %s'%result
    print db.hgetall("party")
    return json.dumps({'message':'success'})
@app.route('/deletethread')
def deletethread():
    instance_id = os.getenv("CF_INSTANCE_INDEX") 
    print 'Instance Id **************%s'%instance_id
    thread_count = int(db.hget("party",instance_id))
    thread_count-=1
    db.hset("party",instance_id,thread_count)
    
    return json.dumps({'message':'success'})

@app.route('/register')
def register():
    mydict = db.hgetall("party")
    print mydict
    mylist = []
#     for k in mydict:
#         if float(mydict[k]) > (time.time() - 1):
#             mylist.append(k)
    return render_template('robots.html', mydict=mydict)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
#     t = threading.Thread(target=heartbeat)
#     t.start()
    init_workers()
    app.run(host='0.0.0.0', port=port, debug=True)
