from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    now = datetime.datetime.now()
    return render_template("index.html", time=now.strftime("%Y-%m-%d %H:%M:%S"))

@app.route("/hello", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        name = request.form.get("name", "Guest")
        return render_template("hello.html", name=name)
    return render_template("hello.html", name="Guest")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)
