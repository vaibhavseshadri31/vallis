import time
from llama_index.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
    SummaryExtractor
)
from llama_index.schema import MetadataMode
from llama_index.node_parser import (
    SentenceSplitter, SemanticSplitterNodeParser)
from llama_index.llms import OpenAI
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    SimpleDirectoryReader
)
from llama_index.embeddings import OpenAIEmbedding
from llama_index.ingestion import IngestionPipeline


# Expensive ass function, try not to run too much (only if we add new docs or want to change up preprocessing strategy)
def build_index():
    PERSIST_DIR = "../storage"
    start = time.time()
    # create nodes and index
    index = VectorStoreIndex(get_nodes())
    end = time.time()

    print("Build time: ", end-start)

    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)


def get_nodes():
    # Get text documents
    documents = SimpleDirectoryReader(
        "../data/txt_files/best_practices").load_data()

    for doc in SimpleDirectoryReader("../data/txt_files/case_studies").load_data():
        documents.append(doc)

    embed_model = OpenAIEmbedding()
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

    pipeline = IngestionPipeline(
        transformations=[
            SemanticSplitterNodeParser(embed_model=embed_model),
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
