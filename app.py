from flask import Flask, request, render_template
import difflib

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
