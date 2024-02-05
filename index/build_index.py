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
from llama_index.ingestion import IngestionPipeline, IngestionCache


# Expensive ass function, try not to run too much (only if we add new docs or want to change up preprocessing strategy)
def build_index():
    PERSIST_DIR = "../storage"

    # create nodes and index
    index = VectorStoreIndex(get_nodes())

    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)


def get_nodes():
    # Get text documents
    documents = SimpleDirectoryReader(
        "../data/txt_files/best_practices").load_data()

    for doc in SimpleDirectoryReader("../data/txt_files/case_studies").load_data():
        documents.append(doc)

    # node_parser = SentenceSplitter(chunk_size=512)
    # extractor = TitleExtractor()

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=20),
            TitleExtractor(),
            QuestionsAnsweredExtractor(
                questions=3, llm=llm, metadata_mode=MetadataMode.EMBED),
            SummaryExtractor(
                summaries=["prev", "self", "next"], llm=llm),
        ]
    )

    nodes = pipeline.run(documents=documents)

    return nodes


if __name__ == '__main__':
    build_index()
