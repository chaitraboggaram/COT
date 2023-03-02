from flask import Flask, render_template, request
import os
import openai
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
import re
# from gensim.summarization import summarize
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

app = Flask(__name__)
new_path = ""
result = ""
plagiarism_result = ""

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

        global new_path
        new_path = os.path.join(app.static_folder, new_filename)
        os.rename(old_path, new_path)

        print(old_path)
        print(new_path)

        message = 'File upload successful!\n\nWait while we calculate the Plagiarism result.'
        # return render_template('index.html', message=message)
        return render_template('alert.html', message=message)

    else:
        # If file1.txt exist open it else create a file1.txt
        with open('static/file1.txt', 'w') as f:
            f.write(str(text))
            message = "Content submittion successful!\n\nWait while we calculate the Plagiarism result."
            return render_template('alert.html', message=message)


@app.route("/check")
def check():
    global plagiarism_result

    sample_files = [doc for doc in os.listdir(app.static_folder) if doc.endswith('.txt')]
    sample_contents = [open(os.path.join(app.static_folder, file)).read() for file in sample_files]              

    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()    
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])             

    vectors = vectorize(sample_contents)
    s_vectors = list(zip(sample_files, vectors))

    plagiarism_result = set()

    for sample_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((sample_a, text_vector_a))
        del new_vectors[current_index]

        for sample_b, text_vector_b in new_vectors:
            similarity_score = round(similarity(text_vector_a, text_vector_b)[0][1], 4)
            sample_pair = sorted((sample_a, sample_b))
            score = sample_pair[0], sample_pair[1], similarity_score
            plagiarism_result.add(score)
    return plagiarism_result
    

@app.route("/chart")
def chart():
    global new_path
    global result

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
    for i in range(0, 5):
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
        # with open('static/file2.txt', 'w') as f:
            f.write(str(var_name))
    results = check()

    plagiarised_content = [t[2] for t in results if 'file1.txt' in t]
    plagiarism_percent = max(plagiarised_content) * 100
    non_plagirism_percent = 100 - plagiarism_percent

    data = [plagiarism_percent, non_plagirism_percent]

    # Removing the files created by chatGPT
    chatGPT_file1_path = os.path.join(app.static_folder, 'chatGPT_file1.txt')
    chatGPT_file2_path = os.path.join(app.static_folder, 'chatGPT_file2.txt')
    chatGPT_file3_path = os.path.join(app.static_folder, 'chatGPT_file3.txt')
    chatGPT_file4_path = os.path.join(app.static_folder, 'chatGPT_file4.txt')
    chatGPT_file5_path = os.path.join(app.static_folder, 'chatGPT_file5.txt')
    os.remove(chatGPT_file1_path)
    os.remove(chatGPT_file2_path)
    os.remove(chatGPT_file3_path)
    os.remove(chatGPT_file4_path)
    os.remove(chatGPT_file5_path)

    return render_template("chart.html", data=data)


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
