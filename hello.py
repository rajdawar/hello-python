import os
import uuid
import redis
import json
import newrelic.agent
from flask import Flask

newrelic.agent.initialize()

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])

app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

COLOR = GREEN

@app.route('/')
def hello():

    r.incr('HITCOUNT')
    PAGEHITS = r.get('HITCOUNT')
    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {}</br>

    {}</br>

    </center>
    
 
   </body>
    </html>
    """.format(COLOR,my_uuid,PAGEHITS)

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
