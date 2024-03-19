import os
from flask import Flask, render_template, request, session
from src.engine import create_engine

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'optional-default-key')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup")
def sign_up():
    return render_template("signup.html")


@app.route("/phil")
def chat():
    return render_template("chatbot.html")


@app.route("/user_data", methods=["GET"])
def store_user_data():

    user_context = request.args.get("text", None)
    if user_context is None:
        return (
            "No text found, please include a ?text=blah parameter in the URL",
            400,
        )
    session["user_context"] = user_context
    return user_context, 200


@app.route("/query", methods=["GET"])
def query_index():

    query_text = request.args.get("text", None)
    if query_text is None:
        return (
            "No text found, please include a ?text=blah parameter in the URL",
            400,
        )

    if "user_context" not in session or session["user_context"] == " ":
        return ("No user context found, please include a user context at /user_data",
                400,
                )

    user_context = session["user_context"]

    chat_engine = create_engine(
        user_context=user_context, storage_dir="./storage")

    response = chat_engine.chat(query_text)

    url_set = set()
    for n in response.source_nodes:
        url_set.add(n.metadata["url"])

    for url in url_set:
        response = str(response) + f"\n {url}"

    return str(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
