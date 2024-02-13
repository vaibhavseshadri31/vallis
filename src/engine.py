from llama_index.llms import ChatMessage, MessageRole
from llama_index.chat_engine.condense_question import (
    CondenseQuestionChatEngine,
)
from llama_index.memory import ChatMemoryBuffer
from llama_index import (
    StorageContext,
    ServiceContext,
    load_index_from_storage,
)
from llama_index.llms import Replicate
from llama_index.response_synthesizers import get_response_synthesizer

from llama_index.prompts import PromptTemplate
from llama_index.llms import ChatMessage, MessageRole
from llama_index.chat_engine.condense_plus_context import (
    CondensePlusContextChatEngine,
)


def create_engine(user_context):

    index = get_index()

    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

    # response_synthesizer = get_response_synthesizer(
    #     response_mode="refine")

    engine = build_chat_engine(index, user_context)
    # engine = index.as_chat_engine(
    #     chat_mode=chat_mode, memory=memory, verbose=True, response_synthesizer=response_synthesizer)

    return engine


def get_index():

    PERSIST_DIR = "../storage"

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

    return index


def build_chat_engine(index, user_context):

    custom_prompt = PromptTemplate(
        """\
    Given a conversation (between Human and Assistant) and a follow up message from Human, \
    rewrite the message to be a standalone question that captures all relevant context \
    from the conversation.

    <Chat History>
    {chat_history}

    <Follow Up Message>
    {question}

    <Standalone question>
    """
    )

    # list of `ChatMessage` objects
    custom_chat_history = [
        ChatMessage(
            role=MessageRole.USER,
            content=user_context
        ),
        ChatMessage(role=MessageRole.ASSISTANT, content="Okay, sounds good."),
    ]

    query_engine = index.as_query_engine()
    retriever = index.as_retriever()
    chat_engine = CondensePlusContextChatEngine.from_defaults(
        query_engine=query_engine,
        retriever=retriever,
        condense_question_prompt=custom_prompt,
        chat_history=custom_chat_history,
        verbose=False,
    )

    return chat_engine


def get_open_source_llm():
    llm = Replicate(
        model="meta/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
        is_chat_model=True,
        additional_kwargs={"max_new_tokens": 512})

    return llm
