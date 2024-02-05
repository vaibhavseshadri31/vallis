
from llama_index.memory import ChatMemoryBuffer
from llama_index import (
    StorageContext,
    load_index_from_storage,
)


def create_engine(chat_mode, engine_type):

    index = get_index()

    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

    if engine_type == "query":
        engine = index.as_query_engine(streaming=True)
    else:
        engine = index.as_chat_engine(
            chat_mode=chat_mode, memory=memory, verbose=True)

    return engine


def get_index():

    PERSIST_DIR = "../storage"

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

    return index
