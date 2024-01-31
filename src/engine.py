import os.path
from pathlib import Path
from llama_index import download_loader
from llama_index.memory import ChatMemoryBuffer
from llama_index.llms import OpenAI
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)


def create_engine(new_store, chat_mode, engine_type):
    # Parse document into chunks according to chunk_size
    service_context = ServiceContext.from_defaults(
        llm=OpenAI(model="gpt-3.5-turbo", temperature=0))

    index = get_index(new_store, service_context)

    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

    if engine_type == "query":
        engine = index.as_query_engine(streaming=True)
    else:
        engine = index.as_chat_engine(
            chat_mode=chat_mode, memory=memory, verbose=True)

    return engine


def get_index(new_store, service_context):
    # check if storage already exists
    PERSIST_DIR = "../storage"
    if new_store or not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = get_docs()

        index = VectorStoreIndex.from_documents(
            documents, service_context=service_context)

        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)

    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    return index


def get_docs():
    # Get text documents
    documents = SimpleDirectoryReader("../data/txt_files").load_data()

    # Get pdf documents
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    pdf_docs = loader.load_data(file=Path('../data/pdf_files/ANN.pdf'))

    for document in pdf_docs:
        documents.append(document)

    return documents
