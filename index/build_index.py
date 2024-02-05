import os.path
from pathlib import Path
from llama_index.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
    SummaryExtractor
)
from llama_index.schema import MetadataMode
from llama_index.node_parser import SentenceSplitter
from llama_index import download_loader
from llama_index.llms import OpenAI
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    SimpleDirectoryReader
)


# Expensive ass function, try not to run too much (only if we add new docs or want to change up preprocessing strategy)
def build_index():
    PERSIST_DIR = "../storage"

    # load the documents and create the index
    documents = get_docs()

    service_context = get_service_context()

    index = VectorStoreIndex.from_documents(
        documents, service_context=service_context)

    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)


def get_docs():
    # Get text documents
    documents = SimpleDirectoryReader("../data/txt_files").load_data()

    # Get pdf documents
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()

    # load data takes a file at a time, cannot take in a directory
    directory = '../data/pdf_files'

    # iterate over files in pdf directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            curr_pdf = loader.load_data(
                file=Path(f))

        for doc in curr_pdf:
            documents.append(doc)

    return documents


# Preprocessing
def get_service_context():

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0)
    text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)

    # Extracts a title from first x nodes in document
    title_extractor = TitleExtractor(nodes=5)

    # Extracts x questions from each node that could be answered
    qa_extractor = QuestionsAnsweredExtractor(
        questions=3, llm=llm, metadata_mode=MetadataMode.EMBED)

    # Extracts a summary from nodes
    summary_extractor = SummaryExtractor(
        summaries=["prev", "self", "next"], llm=llm)

    transformations = [title_extractor, qa_extractor, summary_extractor]

    service_context = ServiceContext.from_defaults(
        llm=llm, text_splitter=text_splitter, transformations=transformations)

    return service_context


if __name__ == '__main__':
    build_index()
