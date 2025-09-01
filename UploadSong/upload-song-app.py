#Import necessary modules from flask, werkzeug, and redis
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import redis
import logging, sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("upload-song-service")
logging.getLogger("werkzeug").setLevel(logging.WARNING)

#Initialize the Flask app with a specified template folder
app = Flask(__name__, template_folder='templates')
#Configure upload folder and allowed file extensions
app.config['UPLOAD_FOLDER'] = 'static/songs'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg'}

# Connect to Redis database with logging
try:
    r = redis.Redis(host='redis-db', port=6379, db=0, decode_responses=True)
    r.ping()
    logger.info("Connected to Redis successfully")
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    raise

def allowed_file(filename):
    #Check if file extension is allowed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload_song():
    if request.method == 'POST':
        #Get uploaded file and song details from form
        file = request.files.get('file')
        author = request.form.get('author')
        year = request.form.get('year')
        duration = request.form.get('duration')
        song_name = request.form.get('song_name') or file.filename

        logger.info(f"Upload attempt: song_name='{song_name}', author='{author}', year='{year}'")

        if not file:
            logger.warning("Upload failed: no file provided")
            return render_template('upload-song.html.j2', message="No file uploaded")

        if not allowed_file(file.filename):
            logger.warning(f"Upload failed: invalid file type '{file.filename}'")
            return render_template('upload-song.html.j2', message="Invalid file type")

        #Ensure filename is secure and save file to upload folder
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        #Prepare and save song details to Redis
        song_data = {
            'filename': filename,
            'author': author,
            'duration': duration,
            'year': year,
            'title': song_name
        }

        #Save song details in Redis using hash set
        r.hset(f'song:{filename}', mapping=song_data)

        logger.info(f"Song uploaded successfully: {song_data}")

        return redirect(url_for('upload_song'))

    #Display upload form for GET request or upon redirect
    return render_template('upload-song.html.j2')

#Start the Flask app on port 5000 in debug mode
if __name__ == "__main__":
    logger.info("Starting upload-song service on 0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

