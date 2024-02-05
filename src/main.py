import logging
import sys
from llama_index.response.notebook_utils import display_source_node
from engine import create_engine


def main():
    # Uncomment these lines for logging

    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    chat_engine = create_engine(chat_mode="condense_plus_context")

    print("\nVallisAI virtual mentor, type \"quit\" when you are done\n")

    while (True):
        query = input(">> ")

        if query == "quit":
            chat_engine.reset()
            return

        # print(chat_engine.chat(query))
        response = chat_engine.stream_chat(query)
        response.print_response_stream()
        for n in response.source_nodes:
            print(len(n.get_content()))
        print("\n")


if __name__ == '__main__':
    main()
