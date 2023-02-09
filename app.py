from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        # Do something with the file (e.g. save it to disk)
        return "File uploaded successfully"
    return """
        <form method="post" enctype="multipart/form-data">
          <div class="form-group">
            <label for="choosefile">Choose File:</label>
            <input type="file" class="form-control-file" id="choosefile" name="file">
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    """

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)


