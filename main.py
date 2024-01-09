#####################
# Building RAG system
######################

# Standard library imports
import os
import pickle

# Related third-party imports
import boto3
import nest_asyncio
import pandas as pd
from dotenv import load_dotenv

# Local application/library-specific imports
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.evaluation import generate_question_context_pairs, RetrieverEvaluator
from llama_index.llms import OpenAI
from llama_index.node_parser import SimpleNodeParser
from llama_index import download_loader

import gradio as gr
# The nest_asyncio module enables the nesting of asynchronous functions within an already running async loop.
# This is necessary because Jupyter notebooks inherently operate in an asynchronous loop.
# By applying nest_asyncio, we can run additional async functions within this existing loop without conflicts.
nest_asyncio.apply()

# # Load environment variables from .env file
load_dotenv()

# using the existing vector index if it exists
vector_path = "/Users/ryanjohnson/Documents/work/roleplaying_rag/vector_index.pkl"

if os.path.exists(vector_path):
    # Load vector_index from the serialized file
    with open('vector_index.pkl', 'rb') as f:
        vector_index = pickle.load(f)
else:
    # Build index with a chunk_size of 512
    # Use the S3 Reader to grab the phb text file
    S3Reader = download_loader("S3Reader")
    loader = S3Reader(bucket='dndragsystem', key='phb5e.txt')
    documents = loader.load_data()
    # Create the index
    node_parser = SimpleNodeParser.from_defaults(chunk_size=512)
    nodes = node_parser.get_nodes_from_documents(documents)
    vector_index = VectorStoreIndex(nodes, show_progress = True)
    # Serialize and save vector_index to a file
    with open('vector_index.pkl', 'wb') as f:
        pickle.dump(vector_index, f)

def stupid_test(message, placeholder):
    print("This is the input text:", message)
    #print("This is the second argument passed in:", placeholder)
    # Build a QueryEngine and start querying.
    query_engine = vector_index.as_query_engine()
    response = query_engine.query(message)
    print(response)
    return str(response)

iface = gr.ChatInterface(
    fn = stupid_test,
    title="The Supreme Modron's All Knowing Repository of Knowledge",
    description="Ask any question about Faerun or about 5th edition rules.")

iface.launch(share=False, inbrowser=True)