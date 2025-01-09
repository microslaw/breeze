from flask import Flask

app = Flask(__name__)

@app.route('/app', methods=['GET'])
def main_page():
    return "test"

app.run(debug = True)

