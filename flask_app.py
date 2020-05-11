import json
import apiai
import os
import mysql.connector
from flask import Flask, render_template
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

import numpy as np
import scipy.special

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show

from bokeh.resources import CDN
from bokeh.embed import file_html


#from bokeh.charts import Histogram
#from bokeh.charts import Histogram

#from flask import Flask, render_template, request
#import pandas as pd
#from bokeh.charts import Histogram
#from bokeh.embed import components

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
mydb = mysql.connector.connect(
    host="atrinh96.mysql.pythonanywhere-services.com",
    user="atrinh96",
    passwd="At1996at!",
    database="atrinh96$test"
)
mycursor = mydb.cursor()
#mycursor.execute("SELECT user FROM Users")
#myresult = mycursor.fetchall()
#feature_names = [ ]
#for users in myresult:
#    feature_names.append(users)



@app.route('/')
def index():
    return render_template("main_page.html")
@app.route("/", methods=['GET', 'POST'])
def serve():
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
    uname = "name"
    return str(uname)

@app.route("/home", methods=['GET', 'POST'])
def home():
    from flask import request
    patro = "bye"
    return str(patro)

@app.route("/data", methods=['GET', 'POST'])
def data():
    hello = "hello"
    return str(hello)

@app.route("/login", methods=['GET', 'POST'])
def login():
    from flask import request
    log = "in the login page"
    uname = request.values.get("uname", None)
    pword = request.values.get("passwd", None)
    mycursor.execute("SELECT user FROM Users;")
    myresult = mycursor.fetchall()
    log += str(myresult)
    feature_names = [ ]
    for users in myresult:
        feature_names.append(users)
    current_feature_name = "Select a user from the scroll bar above"
    current_feature_name = request.args.get("feature_name")


    mycursor.execute("SELECT * FROM Headache WHERE user = %s", (current_feature_name,))
    data = mycursor.fetchall()


#sql = "SELECT * FROM customers WHERE address = %s"
#adr = ("Yellow Garden 2", )

#mycursor.execute(sql, adr)

#myresult = mycursor.fetchall()


    x = [1,2,3,4,5]
    y = [4,6,2,4,3]
    output_file('platform_page.html')
    p = figure(title='Simple Example', x_axis_label='X Axis', y_axis_label='Y Axis')
    p.line(x, y, legend='Test', line_width=2)
    script, div = components(p)

    #return str(log)
    return render_template("platform_page.html", script=script, div=div, feature_names=feature_names, current_feature_name=current_feature_name, data=data)


@app.route("/register", methods=['GET', 'POST'])
def register():
    from flask import request
    uname = request.form['username']
    pword = request.form['password']
    phone = request.form['phone']
    return render_template("login.html")
if __name__ == "__main__":
    app.run(debug=True)