from flask import Flask, render_template, request
import os
import openai
from keybert import KeyBERT
import os                                                                   # We will be accessing the text files
from sklearn.feature_extraction.text import TfidfVectorizer                 # TfidfVectorizer to detect the similarity in text by performing word embedding
from sklearn.metrics.pairwise import cosine_similarity                      # cosine_similarity method to compute the plagarism w

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Building plagiarism detecter
def check_plagiarism(s_vectors, similarity):
    results = set()

    for sample_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((sample_a, text_vector_a))
        del new_vectors[current_index]

        for sample_b, text_vector_b in new_vectors:
            similarity_score = round(similarity(text_vector_a, text_vector_b)[0][1], 4)
            sample_pair = sorted((sample_a, sample_b))
            score = sample_pair[0], sample_pair[1], similarity_score
            results.add(score)
    return results


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

        #Extract keywords into a txt file
        #new_path = r'C:\Users\ztj_u\Desktop\COT-main\static\file_txt.txt'
        with open(new_path, 'r') as file:
            doc = file.read()


        print(doc)
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(doc,
                                             keyphrase_ngram_range=(3, 3),
                                             stop_words='english',
                                             use_mmr=True,
                                             diversity=0.7
                                             )

        print(keywords)
        results = []
        for scored_keywords in keywords:
            for keyword in scored_keywords:
                if isinstance(keyword, str):
                    results.append(keyword)

        print(results)

        #invoke openAI api
        openai.api_key = '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'

        #Set up the prompt for ChatGPT
        prompt = results

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

        #result is stored to the file "result.txt"
        new_path = r'C:\Users\ztj_u\Desktop\COT-main\static\result.txt'
        with open(new_path, 'w') as f:
            # Define the data to be written
            f.write(result)

        #Compute similarity
        directory = r'C:\Users\ztj_u\Desktop\COT-main\static\\'
        sample_files = []
        for doc in os.listdir(directory):
            if doc.endswith('.txt'):
                sample_files.append(directory + doc)

        # Reading the file
        sample_contents = [open(File).read() for File in sample_files]

        # Converting text to array of numbers
        vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
        similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])  # Computing the similarity between two documents

        vectors = vectorize(sample_contents)
        s_vectors = list(zip(sample_files, vectors))

        for data in check_plagiarism(s_vectors, similarity):
            percent = round((data[2] * 100), 2)
            print("Similarity between '" + str(data[0]) + "' and '" + str(data[1]) + "' is " + str(percent) + "%\n")

        #Display the check results
        return render_template('chart.html', message = percent)

    else:
        # If file1.txt exist open it else create a file1.txt
        with open('static/file_txt.txt', 'w') as f:
            f.write(str(text))
            message = "Content submittion successful!"
            return render_template('alert.html', message = message)




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
