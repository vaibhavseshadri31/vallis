import logging
import sys
from engine import create_engine
from llama_index.core import ServiceContext
# from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings
from llama_index.core.chat_engine.types import StreamingAgentChatResponse


def main():
    # Uncomment these lines for logging

    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    print("\nHi there! My name is Phil, your AI mentor created by vallis. Before we start tell me a bit about yourself and your company \n")
    print("Type \"quit\" when you are done\n")
    user_context = input(">> ")
    print("\nIts a pleasure to meet you! How can I help you?\n")

    Settings.llm = OpenAI()
    # Settings.llm = Ollama(model="mistral", request_timeout=120)

    chat_engine = create_engine(
        user_context=user_context, storage_dir="../storage")

    while (True):
        query = input(">> ")
        print("\n")

        if query == "quit":
            chat_engine.reset()
            return

        # print(chat_engine.chat(query))
        response: StreamingAgentChatResponse = chat_engine.stream_chat(query)
        response.print_response_stream()

        url_set = set()
        for n in response.source_nodes:
            url_set.add(n.metadata["url"])

        print("\n")
        print("Here are some useful links regarding your query:\n")
        for url in url_set:
            print(url)
        print("\n")


if __name__ == '__main__':
    main()
