from llama_index.memory import ChatMemoryBuffer
from llama_index import (
    StorageContext,
    ServiceContext,
    load_index_from_storage,
)
from llama_index.llms import Replicate
from llama_index.response_synthesizers import get_response_synthesizer


def create_engine(chat_mode):

    index = get_index()

    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

    response_synthesizer = get_response_synthesizer(
        response_mode="tree_summarize")

    engine = index.as_chat_engine(
        chat_mode=chat_mode, memory=memory, verbose=True, response_synthesizer=response_synthesizer)

    return engine


def get_index():

    PERSIST_DIR = "../storage"

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

    return index


def get_open_source_llm():
    llm = Replicate(
        model="meta/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
        is_chat_model=True,
        additional_kwargs={"max_new_tokens": 512})

    return llm
