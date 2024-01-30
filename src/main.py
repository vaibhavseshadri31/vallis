import os.path
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
import logging
import sys


def main():
    # Uncomment these lines for logging

    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    query_engine = create_query_engine()

    print("\nHelios.ai mentor, type \"quit\" when you are done\n")

    while (True):
        query = input(">> ")

        if query == "quit":
            break

        response = query_engine.query(query)
        print("\n", response, "\n")


def create_query_engine():
    # check if storage already exists
    PERSIST_DIR = "../storage"
    if not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader("../data").load_data()
        index = VectorStoreIndex.from_documents(documents)

        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)

    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    return index.as_query_engine()


if __name__ == '__main__':
    main()
