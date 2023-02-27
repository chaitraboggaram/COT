from flask import Flask, render_template, request
import os
import openai

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
        print("EXIST!")
        filename = file.filename
        old_path = os.path.join(app.static_folder, filename)
        doc_path = os.path.join(app.static_folder, 'file_doc.docx')
        text_path = os.path.join(app.static_folder, 'file_txt.txt')

        if os.path.isfile(doc_path):
            os.remove(doc_path)
        if os.path.isfile(text_path):
            os.remove(text_path)

        # Save the file to the static folder
        print(" path " + os.path.join(app.static_folder, filename))
        file.save(os.path.join(app.static_folder, filename))

        # Getting the file extension
        file_extension = os.path.splitext(filename)[1]

        # Renaming file based on the file extension
        if file_extension == ".docx":
            new_filename = r'file_doc.docx'
        elif file_extension == ".txt":
            new_filename = r'file_txt.txt'
        else:
            message = 'File format not accepted. Choose .txt or .docx file'
            os.remove(old_path)
            return render_template('alert.html', message=message)

        new_path = os.path.join(app.static_folder, new_filename)
        os.rename(old_path, new_path)

        message = 'File upload successful!'
        #return render_template('index.html', message=message)

        #Read the uploaded file in the fold of static
        with open(new_path, 'r') as file:
            text = file.read()

        #invoke openAI api
        openai.api_key = 'sk-QUkhk2NXzY3uJXZcq2rrT3BlbkFJCSOc'

        #Set up the prompt for ChatGPT
        prompt = text

        # Call the completion API and get the response
        response = openai.Completion.create(engine = 'text-davinci-003',
                                            prompt = prompt,
                                            max_tokens = 3000,
                                            temperature = 0.5,
                                            top_p = 1,
                                            frequency_penalty = 0,
                                            presence_penalty = 0
                                            )

        result = response.choices[0].text.strip()

        #Display the check results
        return render_template('chart.html', message=result)

    else:
        # If file1.txt exist open it else create a file1.txt
        with open('static/file_txt.txt', 'w') as f:
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
