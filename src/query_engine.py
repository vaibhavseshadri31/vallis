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

    query_engine = create_engine(
        new_store, chat_mode=None, engine_type="query")

    print("\nHelios Q&A system, type \"quit\" when you are done\n")

    while (True):
        query = input(">> ")

        if query == "quit":
            return

        response = query_engine.query(query)
        response.print_response_stream()
        print("\n")


if __name__ == '__main__':
    main()
