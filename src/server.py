from flask import Flask
from flask import request
from engine import create_engine

app = Flask(__name__)


@app.route("/")
def home():
    return "Vallis"


@app.route("/query", methods=["GET"])
def query_index():
    print("here")

    query_text = request.args.get("text", None)
    if query_text is None:
        return (
            "No text found, please include a ?text=blah parameter in the URL",
            400,
        )
    chat_engine = create_engine("I have a sunglasses company")
    response = chat_engine.chat(query_text)
    return str(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5600)
