import os.path
from llama_index.memory import ChatMemoryBuffer
from llama_index.llms import OpenAI
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
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

    # set to true to update embeddings in storage
    new_store = True

    chat_engine = create_chat_engine(new_store)

    print("\nHelios.ai mentor, type \"quit\" when you are done\n")

    while (True):
        query = input(">> ")

        if query == "quit":
            break

        response = chat_engine.stream_chat(query)
        response.print_response_stream()
        print("\n")

    chat_engine.reset()


def create_chat_engine(new_store):
    # Parse document into chunks according to chunk_size
    service_context = ServiceContext.from_defaults(
        llm=OpenAI(model="gpt-3.5-turbo", temperature=0))

    index = get_index(new_store, service_context)

    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

    chat_engine = index.as_chat_engine(
        chat_mode="condense_plus_context", memory=memory, verbose=False)

    return chat_engine


def get_index(new_store, service_context):
    # check if storage already exists
    PERSIST_DIR = "../storage"
    if new_store or not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader("../data").load_data()
        index = VectorStoreIndex.from_documents(
            documents, service_context=service_context)

        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)

    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    return index


if __name__ == '__main__':
    main()
