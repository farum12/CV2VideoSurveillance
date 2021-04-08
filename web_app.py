import os
from flask import Flask, request, render_template, Response, \
    send_from_directory
from motion_detect import m_d
import time
from datetime import datetime
from database import db_session
from database_handler import getLastSetting, setNewSetting

app = Flask(__name__)
startTime = datetime.now()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png',
                               mimetype='image/vnd.microsoft.icon')

@app.route("/")
def homePage():
    return render_template("welcome.html")

@app.route("/liveFeed")
def liveFeed():
    return render_template("liveFeed.html")

@app.route("/settings")
def settings():
    return render_template("settings.html", currentSettings=getLastSetting())

@app.route("/settings", methods=['POST'])
def my_form_post():
    setNewSetting(request.form['displayTimestamp'],
                  request.form['displayBoundaries'],
                  request.form['analysisMode'],
                  request.form['useYOLO'],
                  request.form.get('area1', 'False'),
                  request.form.get('area2', 'False'),
                  request.form.get('area3', 'False'),
                  request.form['sensitivity'],
                  request.form['maxTicks'])
    return render_template("settings.html", currentSettings=getLastSetting())

@app.route("/about")
def about():
    return render_template("about.html",runtime=getRuntime(),
                           currentSettings=getLastSetting())

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def getRuntime():
    return datetime.now() - startTime

def gen():
    global m_d
    while True:
        #frame = m_d.output_frame
        time.sleep(1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + m_d.output_frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def start():
    app.run(debug=False, use_reloader=False, host="0.0.0.0", port=8080)



