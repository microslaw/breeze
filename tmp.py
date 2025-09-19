#
#  Example usage of ServerSentEvents with Flask.
#  Created On 21 November 2022
#

# to start the server, execute the following command 👇
# python -m flask --app examples/routes run


from flask import Flask
from flask_queue_sse import ServerSentEvents
import time
from threading import Thread

app = Flask(__name__)
sse: ServerSentEvents = None


def spam_requests():
    for i in range(1000):
        time.sleep(1)
        if sse:
            sse.send({"msg": f"message {i}"})
        else:
            print(f"didn't send message {i}")


@app.route("/end")
def end():
    global sse

    if sse:
        sse.send(event="end")
        sse = None
    else:
        return "NO CONNECTION"

    return "FINISHED"


@app.route("/subscribe")
def subscribe():
    global sse

    # create a new server sent events channel
    sse = ServerSentEvents()

    return sse.response()

if __name__ == "__main__":
    thread = Thread(target = spam_requests)
    thread.start()
    app.run()
    thread.join()
