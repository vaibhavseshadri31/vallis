from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.chat_engine.condense_plus_context import (
    CondensePlusContextChatEngine,
)
from llama_index.llms import ollama


def create_engine(user_context):

    index = get_index()

    # response_synthesizer = get_response_synthesizer(
    #     response_mode="refine")

    engine = build_chat_engine(index, user_context)
    # engine = index.as_chat_engine(
    # chat_mode="condense_plus_context", memory=memory, verbose=True)

    return engine


def get_index():

    PERSIST_DIR = "../storage"

    # Pull index from disk
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

    return index


def build_chat_engine(index, user_context):

    # Define how prompts are generated
    custom_prompt = """\
    Given a conversation (between Human and Assistant) and a follow up message from Human, \
    rewrite the message to be a standalone question that captures all relevant context \
    from the conversation.

    <Chat History>
    {chat_history}

    <Follow Up Message>
    {question}

    <Standalone question>
    """ + f" Use this user context to create prompts {user_context}"

    # list of `ChatMessage` objects
    custom_chat_history = [
        ChatMessage(
            role=MessageRole.USER,
            content=user_context
        ),
        ChatMessage(role=MessageRole.ASSISTANT, content="Okay, sounds good."),
    ]

    # configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=2,
    )

    query_engine = index.as_query_engine()
    retriever = retriever
    chat_engine = CondensePlusContextChatEngine.from_defaults(
        query_engine=query_engine,
        retriever=retriever,
        condense_prompt=custom_prompt,
        chat_history=custom_chat_history,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
        verbose=True,
    )

    return chat_engine


def get_open_source_llm():
    llm = ollama(model="mistral")

    return llm
