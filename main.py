import datetime

from flask import Flask, render_template
from flask import request
from src.engine import create_engine

app = Flask(__name__)

user_context = " "


@app.route("/")
def home():

    dummy_times = [
        datetime.datetime(2018, 1, 1, 10, 0, 0),
        datetime.datetime(2018, 1, 2, 10, 30, 0),
        datetime.datetime(2018, 1, 3, 11, 0, 0),
    ]

    return render_template("index.html", times=dummy_times)


@app.route("/user_data", methods=["GET"])
def store_user_data():
    global user_context
    user_context = request.args.get("text", None)
    if user_context is None:
        return (
            "No text found, please include a ?text=blah parameter in the URL",
            400,
        )
    return user_context, 200


@app.route("/query", methods=["GET"])
def query_index():

    query_text = request.args.get("text", None)
    if query_text is None:
        return (
            "No text found, please include a ?text=blah parameter in the URL",
            400,
        )

    global user_context
    if user_context == " ":
        return ("No user context found, please include a user context at /user_data",
                400,
                )

    chat_engine = create_engine(
        user_context=user_context, storage_dir="./storage")

    response = chat_engine.chat(query_text)

    return str(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
