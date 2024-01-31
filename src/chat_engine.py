import logging
import sys

from engine import create_engine


def main():
    # Uncomment these lines for logging

    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    # set to true to update embeddings in storage
    new_store = True

    chat_mode = input(
        "What chatmode will you be using today:\n 1) condense_question\n 2) condense_plus_context\n\n >> ")

    chat_engine = create_engine(
        new_store, chat_mode=chat_mode, engine_type="chat")

    print("\nHelios chatbot, type \"quit\" when you are done\n")

    while (True):
        query = input(">> ")

        if query == "quit":
            chat_engine.reset()
            return

        response = chat_engine.stream_chat(query)
        response.print_response_stream()
        print("\n")


if __name__ == '__main__':
    main()
