import logging
import sys

from engine import create_engine


def main():
    # Uncomment these lines for logging

    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    # DONT CHANGE UNLESS YOU ADD NEW DOCS
    # If set to true, all vector embeddings are recomputed (Lot of requests to OpenAI)
    # --------------------------------------------------------------------------------#
    new_store = False
    # --------------------------------------------------------------------------------#

    chat_mode = input(
        "What chatmode will you be using today:\n 1) condense_question: Your question will be rephrased and passed into the query engine \
        \n 2) condense_plus_context: Your question will be condensed and relevant documents will be passed into GPT 3.5-turbo\n\n >> ")

    chat_engine = create_engine(
        new_store, chat_mode=chat_mode, engine_type="chat")

    print("\nHelios chatbot, type \"quit\" when you are done\n")

    while (True):
        query = input(">> ")

        if query == "quit":
            chat_engine.reset()
            return

        print(chat_engine.chat(query))
        # response = chat_engine.stream_chat(query)
        # response.print_response_stream()
        print("\n")


if __name__ == '__main__':
    main()
