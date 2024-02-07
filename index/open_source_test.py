from llama_index import VectorStoreIndex
from llama_index import ServiceContext
from llama_index.llms import Replicate
from llama_index.prompts import PromptTemplate
import os
from llama_index.readers import BeautifulSoupWebReader
from llama_index.response.notebook_utils import display_response

url = "https://www.theverge.com/2023/9/29/23895675/ai-bot-social-network-openai-meta-chatbots"

documents = BeautifulSoupWebReader().load_data([url])

os.environ["REPLICATE_API_TOKEN"] = "r8_PHi6HrX3quIsp12kB9gmunXpnudGw4d32A8RC"


llm = Replicate(
    model="meta/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
    is_chat_model=True,
    additional_kwargs={"max_new_tokens": 512}
)

service_context = ServiceContext.from_defaults(
    llm=llm, embed_model="local:BAAI/bge-small-en-v1.5")


vector_index = VectorStoreIndex.from_documents(
    documents, service_context=service_context)

query_engine = vector_index.as_query_engine(response_mode="compact")

response = query_engine.query("How do OpenAI and Meta differ on AI tools?")

print(response)
