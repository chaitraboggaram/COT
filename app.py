from flask import Flask, render_template, request
import os
import openai
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from docx import Document
import re

app = Flask(__name__)

data = ""
highlighted_content = ""

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
        if os.path.isfile(os.path.join(app.static_folder, 'logic.txt')):
            os.remove(os.path.join(app.static_folder, 'logic.txt'))

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

        global new_path
        new_path = os.path.join(app.static_folder, new_filename)
        os.rename(old_path, new_path)

        if file_extension == ".docx":
            new_filename = r'file1.docx'

            # Set the path of the docx file and the output txt file
            docx_file_path = os.path.join('static', 'file1.docx')
            txt_file_path = os.path.join('static', 'file1.txt')

            # Open the docx file and extract its text
            doc = Document(docx_file_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

            # Save the text to a txt file with UTF-8 encoding
            with open(txt_file_path, 'w', errors='ignore') as txt_file:
            # with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)

        message = 'File upload successful!\n\nWait while we calculate the Plagiarism result.'
        return render_template('alert.html', message=message)

    else:
        # If file1.txt exist open it else create a file1.txt
        with open('static/file1.txt', 'w') as f:
            f.write(str(text))
            message = "Content submittion successful!\n\nWait while we calculate the Plagiarism result."
            return render_template('alert.html', message=message)


@app.route("/check")
def check():
    global data
    global highlighted_content

    sample_files = [doc for doc in os.listdir(app.static_folder) if doc.endswith('.txt')]

    # Read all files into a list
    files_content = []
    for sample_file in sample_files:
        with open(os.path.join(app.static_folder, sample_file)) as f:
            files_content.append(f.read())

    # Define the vectorizer using the entire corpus of texts
    vectorizer = TfidfVectorizer()
    vectorizer.fit(files_content)

    # Get the content of file1.txt
    with open(os.path.join(app.static_folder, 'file1.txt')) as file1:
        file1_content = file1.read()

    plagiarism_result = set()

    # Compare file1.txt with all other files
    for sample_b in sample_files:
        # Skip file1.txt itself
        if sample_b == 'file1.txt':
            continue

        with open(os.path.join(app.static_folder, sample_b)) as file2:
            file2_content = file2.read()

        # Transform each individual text using the same vectorizer
        file1_vec = vectorizer.transform([file1_content])
        file2_vec = vectorizer.transform([file2_content])

        # Compute similarity score between file1.txt and the current file
        similarity_score = round(cosine_similarity(file1_vec, file2_vec)[0][0], 4)

        # Store the score and file names in the plagiarism_result set
        sample_pair = sorted(('file1.txt', sample_b))
        score = sample_pair[0], sample_pair[1], similarity_score
        plagiarism_result.add(score)

    # Get the max score and the files with the max score
    max_score_val = max(plagiarism_result, key=lambda x: x[2])[2]
    max_files = [(t[0], t[1]) for t in plagiarism_result if t[2] == max_score_val]

    # Get matching content between max_files
    with open(os.path.join(app.static_folder, max_files[0][0])) as file1:
        file1_content = file1.read()
    with open(os.path.join(app.static_folder, max_files[0][1])) as file2:
        file2_content = file2.read()
    match_content = list(set(file1_content.split()) & set(file2_content.split()))

    # Highlight the matched content in file1.txt
    highlighted_content = file1_content
    for match in match_content:
        highlighted_content = re.sub(match, f'<mark >{match}</mark>', highlighted_content)


    plagiarised_content = [t[2] for t in plagiarism_result if 'file1.txt' in t]
    plagiarism_percent = round(max(plagiarised_content) * 100, 2)
    non_plagiarism_percent = 100 - plagiarism_percent

    data = [plagiarism_percent, non_plagiarism_percent]

    return (data, highlighted_content)


@app.route("/chart")
def chart():
    global data
    global highlighted_content

    if os.path.isfile(os.path.join(app.static_folder, 'logic.txt')):
        return render_template("chart.html", data=data, content=highlighted_content)
    else: 
        # Removing the files created by chatGPT
        chatGPT_file1_path = os.path.join(app.static_folder, 'chatGPT_file1.txt')
        chatGPT_file2_path = os.path.join(app.static_folder, 'chatGPT_file2.txt')
        chatGPT_file3_path = os.path.join(app.static_folder, 'chatGPT_file3.txt')
        chatGPT_file4_path = os.path.join(app.static_folder, 'chatGPT_file4.txt')
        chatGPT_file5_path = os.path.join(app.static_folder, 'chatGPT_file5.txt')
        
        if os.path.isfile(chatGPT_file1_path):
            os.remove(chatGPT_file1_path)
            
        if os.path.isfile(chatGPT_file2_path):
            os.remove(chatGPT_file2_path)

        if os.path.isfile(chatGPT_file3_path):
            os.remove(chatGPT_file3_path)

        if os.path.isfile(chatGPT_file4_path):
            os.remove(chatGPT_file4_path)

        if os.path.isfile(chatGPT_file5_path): 
            os.remove(chatGPT_file5_path)

        new_path = os.path.join(app.static_folder, 'file1.txt')

        #Read the uploaded file in the fold of static
        with open(new_path, 'r') as file:
            text = file.read()

        #invoke openAI api
        openai.api_key = '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'
        
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)

        # The first sentence is usually the title
        title = sentences[0]

        # Pass the title as the prompt to OpenAI
        prompt = f"Write an essay on '{title}'."

        # Call the completion API and get the response
        for i in range(0, 2):
            if i > 0:
                prompt = f"Write an essay on '{title}, give a different content for this'."

            var_name = f"var{i+1}"

            response = openai.Completion.create(engine = 'text-davinci-003',
                                                prompt = prompt,
                                                max_tokens = 3000,
                                                temperature = 0.5,
                                                top_p = 1,
                                                frequency_penalty = 0,
                                                presence_penalty = 0
                                                )

            var_name = response.choices[0].text.strip()
            file_name = f"chatGPT_file{i+1}.txt"
            file_path = 'static/' + file_name
            with open(file_path, 'w') as f:
                f.write(str(var_name))
        data, highlighted_content = check()

        with open(os.path.join(app.static_folder, 'logic.txt'), 'w') as f:
            f.write("Logic created")

        return render_template("chart.html", data=data, content=highlighted_content)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/terms')
def terms():
    return render_template('terms_and_conditions.html')


@app.route("/teamcot")
def teamcot():
    return render_template("teamcot.html")


@app.route("/aboutplagiarism")
def aboutplagiarism():
    return render_template("aboutplagiarism.html")

if __name__ == '__main__':
    app.run(debug=True)
