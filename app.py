from flask import Flask, render_template
from graduation import *
import os

flask_app = Flask(__name__)
flask_app.register_blueprint(graduation)

@flask_app.route("/")
def index():
    data = {
        "title": "Vliegen - Homepage",
        "selected": "index"
    }
    return render_template("home.html", data=data)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    flask_app.run(host='0.0.0.0', port=port, debug=True)
