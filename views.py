"""
Routes and views for the flask application.
"""


import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory


from datetime import datetime
from flask import render_template, request
from FlaskWebProject2 import app
from flask import send_file



posts = [{
    'title': 'Music Management system',
    'text': 'Play a song',
    'file': "2.mp3"
}]


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html', posts=posts,
        title='Home Page',
        year=datetime.now().year,
    )


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'.mp3'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return ...


@app.route('/uploads/<filename>')

def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    
  
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def search():
    return render_template('delete_files.html')

@app.route('/remove/<file_id>')
def remove(file_id):
    filename_csv = f"{file_id}.mp3"
    try:
        os.remove(uploaded_file)
        return "Files are deleted successfully"
    except Exception as e:
        return f"Error in deleting files: {e}"


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        text = request.form['text']

        import os
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"

        from google.cloud import texttospeech
        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.types.SynthesisInput(text=text)
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            name='en-US-Standard-C',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        response = client.synthesize_speech(input_text, voice, audio_config)

        # The response's audio_content is binary.
        with open('/tmp/output.mp3', 'wb') as out:
            out.write(response.audio_content)

        return send_file("/tmp/output.mp3")
    else:
        return render_template("hello_form.html")




