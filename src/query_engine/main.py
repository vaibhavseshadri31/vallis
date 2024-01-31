import logging
import sys

from query_engine import create_query_engine


def main():
    # Uncomment these lines for logging

    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    # set to true to update embeddings in storage
    new_store = True

    query_engine = create_query_engine(new_store)

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
