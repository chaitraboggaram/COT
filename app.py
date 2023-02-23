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

    # Get textbox from the form
    text = request.form.get('textbox')

    # Checking if content is available for checking
    if not file and not text:
        message = "Error! No file or text provided"
        return render_template('alert.html', message=message)

    # If file is uploaded
    if file:
        filename = file.filename
        old_path = os.path.join(app.static_folder, filename)
        doc_path = os.path.join(app.static_folder, 'file1.docx')
        text_path = os.path.join(app.static_folder, 'file1.txt')

        if os.path.isfile(doc_path):
            os.remove(doc_path)
        if os.path.isfile(text_path):
            os.remove(text_path)

        # Save the file to the static folder
        file.save(os.path.join(app.static_folder, filename))

        # Getting the file extension
        file_extension = os.path.splitext(filename)[1]

        # Renaming file based on the file extension
        if file_extension == ".docx":
            new_filename = r'file1.docx'
        elif file_extension == ".txt":
            new_filename = r'file1.txt'
        else:
            message = 'File format not accepted. Choose .txt or .docx file'
            os.remove(old_path)
            return render_template('alert.html', message=message)

        new_path = os.path.join(app.static_folder, new_filename)
        os.rename(old_path, new_path)

        message = 'File upload successful!'
        # return render_template('index.html', message=message)
        return render_template('alert.html', message=message)

    else:
        # If file1.txt exist open it else create a file1.txt
        with open('static/file1.txt', 'w') as f:
            f.write(str(text))
            message = "Content submittion successful!"
            return render_template('alert.html', message=message)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/terms')
def terms():
    return render_template('terms_and_conditions.html')


@app.route("/chart")
def chart():
    data = [30, 70]
    return render_template("chart.html", data=data)


@app.route("/teamcot")
def teamcot():
    return render_template("teamcot.html")


@app.route("/aboutplagiarism")
def aboutplagiarism():
    return render_template("aboutplagiarism.html")

if __name__ == '__main__':
    app.run(debug=True)
