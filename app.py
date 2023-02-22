from flask import Flask, request, render_template, send_file, send_from_directory
import difflib
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), 'Downloads')

# Ensure the upload and download folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/check', methods=['POST'])
def check():
    text = request.form['text']
    if not text:
        return render_template('home.html')
    text_lines = text.splitlines()
    with open('original_text.txt') as f:
        original_text_lines = f.read().splitlines()
    s = difflib.SequenceMatcher(None, original_text_lines, text_lines)
    ratio = s.ratio()
    if ratio > 0.5:
        results = f'This text is {ratio*100:.2f}% similar to the original text'
    else:
        results = 'This text is not plagiarized'
    return render_template('home.html', results=results)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return render_template('download.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(filepath, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
