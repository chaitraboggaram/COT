''' We will install scikit a machine learning libarary for checking the text similarities
To install the scikit run this command in the terminal           --> "pip install -U scikit-learn"
This command can be run directly on the Visual studio code terminal.            '''

# This file is used when we want to compare the similiarity between the local copy of files in the current folder


import os                                                       # We will be accessing the text files
from sklearn.feature_extraction.text import TfidfVectorizer     # TfidfVectorizer to detect the similarity in text by performing word embedding 
from sklearn.metrics.pairwise import cosine_similarity          # cosine_similarity method to compute the plagarism with vectors

sample_files = [doc for doc in os.listdir() if doc.endswith('.txt')]        # listdir looks for the local directory which the file is in for documents end with .txt
sample_contents = [open(File).read() for File in sample_files]              # Reading the file

vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()    # Converting text to array of numbers
similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])             # Computing the similarity between two documents

vectors = vectorize(sample_contents)
s_vectors = list(zip(sample_files, vectors))


# Building plagiarism detecter
def check_plagiarism():
    results = set()
    global s_vectors

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


for data in check_plagiarism():
    percent = round((data[2] * 100), 2)
    print("Similarity between '" + str(data[0]) + "' and '" + str(data[1]) + "' is " + str(percent) + "%\n")


