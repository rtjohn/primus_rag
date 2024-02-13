import gradio as gr
import os
from llama_index.llms import OpenAI
from llama_index import StorageContext, load_index_from_storage
from llama_index.response.notebook_utils import display_response

# Load vector_index from the serialized file
PERSIST_DIR = "./storage"
storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
vector_index = load_index_from_storage(storage_context)

# Access the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
# Define an LLM
llm_gpt4 = OpenAI(model="gpt-4", api_key=openai_api_key)

# Basic UI 
def interface_func(message, placeholder):
    print("This is the input text:", message)
    # Build a QueryEngine and start querying.
    query_engine = vector_index.as_query_engine()
    # Callbert
    # Reranking
    response = query_engine.query(message)
    print(response)
    return str(response)

iface = gr.ChatInterface(
    fn = interface_func,
    title="The Supreme Modron's All Knowing Repository of Knowledge",
    description="Ask any question about Faerun or about 5th edition rules.")

iface.launch(share=False, inbrowser=True)



