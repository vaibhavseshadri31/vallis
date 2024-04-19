import os
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
from src.engine import create_engine
from llama_index.core.chat_engine.types import StreamingAgentChatResponse

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'optional-default-key')
socketio = SocketIO(app)


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


@socketio.on('send_message')
def handle_message(data):
    user_message = data['message']
    user_context = session.get("user_context", "")
    # Placeholder for where the chat engine processes the message
    # This should be defined in your src.engine module
    chat_engine = create_engine(
        user_context=user_context, storage_dir="./storage")
    response = chat_engine.chat(user_message)

    url_set = set()
    for n in response.source_nodes:
        # Hack to remove last two characters in metadata
        url_set.add(n.metadata["url"][:-2])

    response_with_urls = response.response
    for url in url_set:
        response_with_urls = response_with_urls + url

    emit('receive_message', {'message': response_with_urls})


if __name__ == '__main__':
    socketio.run(app, debug=True)
