from flask import Flask
from flask import request
from engine import create_engine

app = Flask(__name__)

user_context = " "


@app.route("/")
def home():
    return "Vallis"


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
    if user_context == " ":
        return ("No user context found, please include a user context at /user_data",
                400,
                )

    chat_engine = create_engine(user_context)
    response = chat_engine.chat(query_text)
    return str(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5600)
