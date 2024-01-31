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


def create_chat_engine(new_store, chat_mode):
    # Parse document into chunks according to chunk_size
    service_context = ServiceContext.from_defaults(
        llm=OpenAI(model="gpt-3.5-turbo", temperature=0))

    index = get_index(new_store, service_context)

    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

    chat_engine = index.as_chat_engine(
        chat_mode=chat_mode, memory=memory, verbose=True)

    return chat_engine


def get_index(new_store, service_context):
    # check if storage already exists
    PERSIST_DIR = "../../storage"
    if new_store or not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader("../../data").load_data()
        index = VectorStoreIndex.from_documents(
            documents, service_context=service_context)

        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)

    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    return index
