#!flask/bin/python
import json
from flask import Flask, Response, render_template, request, redirect
#from helloworld.flaskrun import flaskrun

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def url():
    form = request.form
    if request.method == 'POST':
        longurl = request.form.get('url')
        print("longurl --> " + longurl)
        return render_template("home.html", short_url=longurl)
    return render_template("home.html")

@application.route('/<short_url>')
def redirect_short_url(short_url):
    print("redirecting to  --> " + short_url)
    return redirect("https://github.com/narenaryan/Pyster/blob/master/templates/home.html")
  
    
if __name__ == '__main__':
    #flaskrun(application)
    #application.run()
    application.run(
        debug="true",
        host="127.0.0.1",
        port=8080
    )
