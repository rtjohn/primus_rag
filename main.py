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
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, StorageContext, download_loader, load_index_from_storage
from llama_index.evaluation import generate_question_context_pairs, RetrieverEvaluator
from llama_index.llms import OpenAI
from llama_index.node_parser import SimpleNodeParser

import logging
import sys

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
#logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

import gradio as gr
# The nest_asyncio module enables the nesting of asynchronous functions within an already running async loop.
# This is necessary because Jupyter notebooks inherently operate in an asynchronous loop.
# By applying nest_asyncio, we can run additional async functions within this existing loop without conflicts.
#nest_asyncio.apply()

# # Load environment variables from .env file
load_dotenv()

# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # Use the S3 Reader to load all the documents
    S3Reader = download_loader("S3Reader")
    loader = S3Reader(bucket='dndragsystem')
    documents = loader.load_data() #1
    # Parse nodes
    #node_parser = SimpleNodeParser.from_defaults(chunk_size=512) 
    #nodes = node_parser.get_nodes_from_documents(documents)
    # Create the index
    #vector_index = VectorStoreIndex(nodes, show_progress = True) #2A
    #vector_index = VectorStoreIndex.from_documents(documents, show_progress = True) #2B
    service_context = ServiceContext.from_defaults(chunk_size=200) #2C
    vector_index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True) #2C
    # Store it for later
    vector_index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# Query the index
query_engine = index.as_query_engine(similarity_top_k=3) #3
response = query_engine.query("What did the author do growing up?") #4
print(response) #5



# UI Stuff
def stupid_test(message, placeholder):
    print("This is the input text:", message)
    # print("This is the second argument passed in:", placeholder)
    # Build a QueryEngine and start querying.
    # Look up Lance DB
    query_engine = vector_index.as_query_engine()
    # Callbert
    # Reranking
    response = query_engine.query(message)
    print(response)
    return str(response)

iface = gr.ChatInterface(
    fn = stupid_test,
    title="The Supreme Modron's All Knowing Repository of Knowledge",
    description="Ask any question about Faerun or about 5th edition rules.")

iface.launch(share=False, inbrowser=True)