import time
import torch

from llama_index.llms import Replicate
from llama_index.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
    SummaryExtractor,
    KeywordExtractor,
    EntityExtractor
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
from llama_index.ingestion.cache import RedisCache, IngestionCache


# Expensive ass function, try not to run too much (only if we add new docs or want to change up preprocessing strategy)
# Add cache and parallel processing
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

    pipeline = create_ingestion_pipeline()

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
            TitleExtractor(llm=llm),
            QuestionsAnsweredExtractor(
                questions=3, metadata_mode=MetadataMode.EMBED, llm=llm),
            SummaryExtractor(
                summaries=["prev", "self", "next"], llm=llm),
            KeywordExtractor(keywords=10, llm=llm),
            EntityExtractor(prediction_threshold=0.5, llm=llm)
        ], cache=ingest_cache
    )

    return pipeline


def get_open_source_llm():
    llm = Replicate(
        model="meta/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
        is_chat_model=True,
        additional_kwargs={"max_new_tokens": 512})

    return llm


if __name__ == '__main__':
    build_index()
