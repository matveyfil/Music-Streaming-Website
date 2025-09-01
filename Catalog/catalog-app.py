#Import necessary libraries
from flask import Flask, render_template, request, make_response, json, session
import redis
import os
import logging, sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("catalog-service")
logging.getLogger("werkzeug").setLevel(logging.WARNING)

#Set up Flask app and Redis connection
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "fallback-secret")  #Secure key for session management

# Connect to Redis database with logging
try:
    r = redis.Redis(host='redis-db', port=6379, db=0, decode_responses=True)
    r.ping()
    logger.info("Connected to Redis successfully")
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    raise

#Route for displaying the song catalog with optional search
@app.route('/catalog', methods=['GET'])
def list_songs():
    search_query = request.args.get('search', '').lower()  #Get search term from query
    song_keys = r.keys('song:*')  #Find all song keys in Redis
    songs = []  #List to hold songs that match search

    #Filter songs by search term
    for song_key in song_keys:
        song = r.hgetall(song_key)
        if search_query in song.get('title', '').lower():
            songs.append(song)

    logger.info(f"Catalog search: query='{search_query}', results={len(songs)}")

    #Render the catalog page with filtered songs
    return render_template('catalog.html.j2', songs=songs)

#Route for displaying details of a specific song
@app.route('/song/<song_id>', methods=['GET'])
def song_details(song_id):
    song_info = r.hgetall(f'song:{song_id}')  #Get song info by ID
    if not song_info:
        logger.warning(f"Song not found: id={song_id}")
        return "Song not found", 404  #Return 404 if song not found

    #Retrieve or initialize song history cookie
    song_history = request.cookies.get('song_history', '[]')
    songs = json.loads(song_history)

    song_title = song_info.get('title', 'Unknown Song')  #Default song title if not set

    #Record song view with user info if logged in, else as anonymous
    if 'username' in session:
        user = session['username']
    else:
        user = "Anonymous"

    logger.info(f"Song viewed: id={song_id}, title='{song_title}', user={user}")
    
    song_entry = {'title': song_title, 'user': user}
    songs.insert(0, song_entry)  #Add to the beginning of history
    songs = songs[:10]  #Keep only the last 10 views

    #Prepare response with song details and update song history cookie
    resp = make_response(render_template('song_detail.html.j2', song=song_info))
    resp.set_cookie('song_history', json.dumps(songs), max_age=30*24*60*60)  #Cookie expires in 30 days
    
    return resp

#Start the app in debug mode on port 5000
if __name__ == '__main__':
    logger.info("Starting catalog service on 0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

