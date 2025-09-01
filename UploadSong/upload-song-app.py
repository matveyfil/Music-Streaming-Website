#Import necessary modules from flask, werkzeug, and redis
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import redis

#Initialize the Flask app with a specified template folder
app = Flask(__name__, template_folder='templates')
#Configure upload folder and allowed file extensions
app.config['UPLOAD_FOLDER'] = 'static/songs'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg'}

#Connect to Redis database
r = redis.Redis(host='redis-db', port=6379, decode_responses=True)

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

        if file and allowed_file(file.filename):
            #Ensure filename is secure and save file to upload folder
            filename = secure_filename(file.filename)
            file_path = '/'.join([app.config['UPLOAD_FOLDER'], filename])
            file.save(file_path)
            
            #Prepare and save song details to Redis
            song_data = {
                'filename': filename, 
                'author': author,
                'duration': duration,
                'year': year,
                'title': song_name  #Use provided song name or filename
            }

            #Save song details in Redis using hash set
            for field, value in song_data.items():
                r.hset(f'song:{filename}', field, value)

            #Redirect to upload page after successful upload
            return redirect(url_for('upload_song'))
    #Display upload form for GET request or upon redirect
    return render_template('upload-song.html.j2')

#Start the Flask app on port 5000 in debug mode
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

