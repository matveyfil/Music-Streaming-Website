#Import Flask and necessary utilities
from flask import Flask, render_template_string, send_from_directory
import os

#Initialize Flask app
app = Flask(__name__)

def load_template(template_name):
    #Load an HTML template from the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))  #Find script directory
    template_path = os.path.join(script_dir, template_name)  #Build path to template
    with open(template_path, 'r') as file:  #Open and read template file
        return file.read()

@app.route('/home')
def index():
    #Serve the main page with a dynamic title
    template_content = load_template("main.html.j2")  #Load HTML template
    return render_template_string(template_content, title="Welcome to the main page")

@app.route('/images/<filename>')
def send_image(filename):
    #Serve images from the 'images' folder
    images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
    return send_from_directory(images_folder, filename)  #Send requested image file

#Run the app in development mode on port 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

