from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the file from the form
    file = request.files['file']
    
    # Save the file to the static folder
    filename = file.filename
    file.save(os.path.join(app.static_folder, filename))

    return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
