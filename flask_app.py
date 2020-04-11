import json
import apiai
import os
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
#from flask_app import db
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# Twilio account info
account_sid = "ACa18e8f3b69e50ff592fac7bde0bc11e4"
auth_token = "c57847ffe70526a225a972b190249f75"
account_num = "+16267885185"
#Twilio server connection
proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}
client = Client(account_sid, auth_token, http_client=proxy_client)

# api.ai account info
CLIENT_ACCESS_TOKEN = "746bcfef28a342568b3feb7d67e05eca"
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

# database setup info
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://atrinh96:At1996at!@atrinh96.mysql.pythonanywhere-services.com/atrinh96$chatbot".format(
    username="atrinh96",
    password="At1996at!",
    hostname="atrinh96.mysql.pythonanywhere-services.com",
    databasename="atrinh96$chatbot",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
#db.create_all()

#@app.route('/hello')
@app.route('/')
def index():
    return render_template("main_page.html")


@app.route("/", methods=['GET', 'POST'])
def boobs():
    from flask import request
    # get SMS metadata
    msg_from = request.values.get("From", None)
    msg = request.values.get("Body", None)
    # prepare API.ai request
    req = ai.text_request()
    req.lang = 'en'  # optional, default value equal 'en'
    req.query = msg
    # get response from API.ai
    api_response = req.getresponse()
    responsestr = api_response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    reply="Hello"
    if 'result' in response_obj:
        response = response_obj["result"]["fulfillment"]["speech"]
        # send SMS response back via twilio
        reply=client.messages.create(to=msg_from, from_= account_num, body=response)
        comment = Comment(id= 0,content="hewloo world!")
        db.session.add(comment)
        db.session.commit()
    #reply="time to cleanse"
    #get values that user posted; inorder to redirect to the home page=?login=successful

    return redirect("/home")
    #return str(reply)

@app.route("/home", methods=['GET', 'POST'])
def vagina():
    from flask import request
    patro = "bye"
    return str(patro)


if __name__ == "__main__":
    app.run(debug=True)
