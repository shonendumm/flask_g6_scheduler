from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    time = datetime.now()
    data = time
    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run()
