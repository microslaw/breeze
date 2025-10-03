#
#  Example usage of ServerSentEvents with Flask.
#  Created On 21 November 2022
#

# to start the server, execute the following command 👇
# python -m flask --app examples/routes run


from flask import Flask
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])


@app.route("/stream")
def stream():
    def get_data():
        while True:
            time.sleep(1)
            yield f"data: The time is {time.ctime()}\n\n"

    return app.response_class(get_data(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run()
