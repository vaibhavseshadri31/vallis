import time
import torch
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
    SummaryExtractor,
    KeywordExtractor
)
from llama_index.core.schema import MetadataMode
from llama_index.core.node_parser import (
    SentenceSplitter, SemanticSplitterNodeParser)
from llama_index.llms.openai import OpenAI
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.ingestion.cache import IngestionCache
from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache


# Expensive ass function, try not to run too much (only if we add new docs or want to change up preprocessing strategy)
# Add parallel processing
def build_index():
    PERSIST_DIR = "../storage"
    start = time.time()
    # create nodes and index
    nodes = get_nodes()

    # exclude certain metadata keys from being seen by LLM
    for node in nodes:
        node.excluded_embed_metadata_keys = [
            "url", "file_path", "file_name", "file_type", "file_size", "creation_date", "last_modified_date", "last_accessed_date"]
        # print(node.get_content(metadata_mode=MetadataMode.EMBED))

    index = VectorStoreIndex(nodes)
    end = time.time()

    print("Build time: ", end-start)

    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)


def get_docs():
    # Get text documents
    documents = SimpleDirectoryReader(
        "../data/txt_files/best_practices").load_data()

    for doc in SimpleDirectoryReader("../data/txt_files/case_studies").load_data():
        documents.append(doc)

    for doc in SimpleDirectoryReader("../data/txt_files/blogs").load_data():
        documents.append(doc)

    for doc in documents:
        # extract url from doc
        content = doc.get_content()
        start_index_url = content.find("https://")
        end_index_url = content.find("\n", start_index_url)
        url = content[start_index_url: end_index_url]
        doc.metadata.update({"url": url})

        doc.excluded_embed_metadata_keys = [
            "file_path", "file_name", "file_type", "file_size", "creation_date", "last_modified_date", "last_accessed_date"]

    return documents


def get_nodes():
    documents = get_docs()

    pipeline = create_ingestion_pipeline()

    # Run ingestion pipeline with specified transformations
    nodes = pipeline.run(documents=documents)

    return nodes


def create_ingestion_pipeline():

    # If cuda is available add parameter device="cuda" in EntityExtractor
    cuda_available = torch.cuda.is_available()

    embed_model = OpenAIEmbedding()

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

    ingest_cache = IngestionCache(
        cache=RedisCache.from_host_and_port(host="127.0.0.1", port=6379),
        collection="my_test_cache",
    )

    # llm = get_open_source_llm()

    pipeline = IngestionPipeline(
        transformations=[
            SemanticSplitterNodeParser(embed_model=embed_model, llm=llm),
            TitleExtractor(llm=llm, embed_model=embed_model, nodes=3),
            QuestionsAnsweredExtractor(
                questions=5, metadata_mode=MetadataMode.EMBED, llm=llm),
            SummaryExtractor(
                summaries=["prev", "self", "next"], llm=llm),
            KeywordExtractor(keywords=10, llm=llm),
            # EntityExtractor(prediction_threshold=0.5, llm=llm)
        ], cache=ingest_cache
    )

    return pipeline


if __name__ == '__main__':
    build_index()
