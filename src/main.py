import logging
import sys

from engine import create_engine


def main():
    # Uncomment these lines for logging

    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    user_input = input(
        "What chatmode will you be using today:\n Type '1' for condense_question: Your question will be rephrased and passed into the query engine \
        \n Type '2' for condense_plus_context: Your question will be condensed and relevant documents will be passed into GPT 3.5-turbo\n\n >> ")

    if user_input == "1":
        chat_mode = "condense_question"
    else:
        chat_mode = "condense_plus_context"

    chat_engine = create_engine(chat_mode=chat_mode, engine_type="chat")

    print("\nHelios chatbot, type \"quit\" when you are done\n")

    while (True):
        query = input(">> ")

        if query == "quit":
            chat_engine.reset()
            return

        # print(chat_engine.chat(query))
        response = chat_engine.stream_chat(query)
        response.print_response_stream()
        print("\n")


if __name__ == '__main__':
    main()
