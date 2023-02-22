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
    old_path = os.path.join(app.static_folder, filename)
    file.save(os.path.join(app.static_folder, filename))

    print(filename)

    # Getting the file extension
    file_extension = os.path.splitext(filename)[1]
    print(file_extension)

    # Renaming file based on the file extension
    if file_extension == ".docx":
        new_filename = r'file1.docx'
    elif file_extension == ".txt":
        new_filename = r'file1.txt'
    else:
        message = 'Choose .txt or .doc file'
        return render_template('index.html', message=message)

    new_path = os.path.join(app.static_folder, new_filename)
    os.rename(old_path, new_path)

    return 'File uploaded successfully'

@app.route('/rename-file')
def rename_file():
    # Get the path to the file to be renamed
    old_filename = 'old_file_name.txt'
    old_path = os.path.join(app.static_folder, old_filename)

    # Create the new filename
    new_filename = 'new_file_name.txt'
    new_path = os.path.join(app.static_folder, new_filename)

    # Rename the file
    os.rename(old_path, new_path)

    return 'File renamed successfully'

if __name__ == '__main__':
    app.run(debug=True)
