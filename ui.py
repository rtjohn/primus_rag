import gradio as gr
import pickle
import os
from dotenv import load_dotenv
from llama_index.llms import OpenAI
from llama_index import LLMPredictor
import time
from llama_index.response.notebook_utils import display_response

# Load vector_index from the serialized file
with open('vector_index.pkl', 'rb') as f:
    index = pickle.load(f)
    
# Access the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
# Define an LLM
llm_gpt4 = OpenAI(model="gpt-4", api_key=openai_api_key)

def test_chat(message, history):
    # Load vector_index from the serialized file
    with open('vector_index.pkl', 'rb') as f:
        index = pickle.load(f)
    #query_engine = vector_index.as_query_engine()
    chat_engine = index.as_chat_engine()
    #response = query_engine.query(message)
    response = chat_engine.query(message)
    return response.response

demo = gr.ChatInterface(fn=test_chat)
demo.launch()






