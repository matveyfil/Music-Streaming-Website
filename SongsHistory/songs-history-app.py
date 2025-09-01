#Import necessary modules from flask
from flask import Flask, request, render_template, json

#Create a Flask application instance
app = Flask(__name__)

@app.route('/history')
def history():
    #Retrieve the song history from cookies, defaulting to an empty list if not found
    song_history = request.cookies.get('song_history', '[]')
    #Convert the JSON string from the cookies into a Python list
    songs = json.loads(song_history)

    #Render the song history template, passing the list of songs to it
    return render_template('songs-history.html.j2', songs=songs)

#Run the application if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

