from llama_index import VectorStoreIndex, SimpleDirectoryReader
import logging
import sys

# Uncomment these lines for logging

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

query = input("What can I assist you with?\n")
response = query_engine.query(query)
print(response)

query = input("Anything else?\n")
response = query_engine.query(query)
print(response)
