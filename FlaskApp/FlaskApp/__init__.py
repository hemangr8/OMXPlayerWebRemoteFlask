import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, url_for
import paramiko
import getpass

#These are the credentials of the Raspberry Pi's ssh connection.
#'hostname' can differ if the IP of the device has changed.

hostname = 'XXX.XXX.XXX.XXX' #Your IP
username = 'pi' #Your Raspberry Pi username
password = '**********' #Your RAspberry Pi password
port = 22


app = Flask(__name__)


#Render the Index page of the remote
@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if "meetbtn" in request.form:
            return render_template('meet.html')
        elif "playerbtn" in request.form:
            return render_template('musicplayer.html')
    else:
        return render_template('index.html')


#Render the music control page with buttons to control OMXPLAYER
@app.route("/musicplayer/", methods=['POST'])
def control():
    try:
#Establishing Connection via paramiko ssh client
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.load_system_host_keys()
        s.connect(hostname, port, username, password)
        if "playbtn" in request.form:
#Calling the script to play songs from folder
            si, so, se = s.exec_command('cd ~/bin ; ./playloop.sh /home/pi/Music/')
            msg = "Playing"
            return render_template('musicplayer.html', message=msg)
        elif "pausebtn" in request.form:
#Calling the script toggle pause
            si, so, se = s.exec_command('cd ~/bin ; ./pause.sh')
            msg = "Paused"
            return render_template('musicplayer.html', message=msg)
        elif "nextbtn" in request.form:
#Calling script to play next song in queue
            si, so, se = s.exec_command('cd ~/bin ; ./qplay.sh')
            msg = "Next"
            return render_template('musicplayer.html', message=msg)
    except Exception, e:
        return render_template('index.html', message=e)


if __name__ == "__main__":
    app.run(debug=True)

