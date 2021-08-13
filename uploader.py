from flask import Flask, render_template, request, redirect, abort
import speech_recognition as sr
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["20 per day", "5 per hour"]
)

@app.route("/")
@limiter.exempt
def index():
    return render_template("index.html")

@limiter.limit("2 per hour")
@app.route("/upload", methods = ["GET", "POST"])
def upload():
    transcript = ""
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        print("Form data rec'd.")

        # check if input file exists
        if "file" not in request.files:
            return abort(400)

        # if file exists get files data
        file = request.files["file"]
        # if file name is blank
        if file.filename == "":
            return abort(400)
        
    
        if file:
            # instantiate a recognizer 
            recognizer = sr.Recognizer()
            # create audiofile for speech recog can process
            audioFile = sr.AudioFile(file)
            # pass the converted audiofile to record and use speech recognition to convert to string
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key = None)
            print(transcript)
        
        return render_template("index.html", transcript = transcript)


if __name__ == "__main__":
    app.run(host="localhost", port=3000)