from llama_index import VectorStoreIndex, SimpleDirectoryReader
import logging
import sys

# Uncomment these lines for logging

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

print("\nHelios.ai mentor, type \"quit\" when you are done\n")

while (True):
    query = input(">> ")

    if query == "quit":
        break

    response = query_engine.query(query)
    print("\n", response, "\n")
