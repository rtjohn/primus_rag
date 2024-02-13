#####################
# Building RAG system
######################

# Standard library imports
import os
import logging
import sys

# Third-party imports
import pandas as pd
from dotenv import load_dotenv
import gradio as gr

# Local application/library-specific imports
from llama_index import VectorStoreIndex, ServiceContext, StorageContext, download_loader, load_index_from_storage
from llama_index.evaluation import generate_question_context_pairs
from llama_index.llms import OpenAI
from llama_index.node_parser import SimpleNodeParser

# Turning logging off for now until I release this publically.
#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
#logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# # Load environment variables from .env file
load_dotenv()

llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(chunk_size=200, llm=llm)

# Check if index is already stored already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # Use the S3 Reader to load all the documents
    S3Reader = download_loader("S3Reader")
    loader = S3Reader(bucket='dndragsystem')
    documents = loader.load_data() #1
    
    #  Having trouble loading the GB vector index, but storing it as a pickly file seems to work?
    #with open('vector_index.pkl', 'rb') as f:
    #    vector_index = pickle.load(f)
    
    # Parse nodes -  not sure how these lines are improving system?
        #node_parser = SimpleNodeParser.from_defaults(chunk_size=512) 
        #nodes = node_parser.get_nodes_from_documents(documents)
        # Create the index form nodes
        #vector_index = VectorStoreIndex(nodes, show_progress = True) #2A
    
    vector_index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True) #2B
    # Store it for later
    vector_index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    vector_index = load_index_from_storage(storage_context, service_context=service_context)
    
    # Serialize and save vector_index to a file
    #with open('vector_index.pkl', 'wb') as f:
    #    pickle.dump(vector_index, f)

# Query the index
query_engine = vector_index.as_query_engine(similarity_top_k=3) #3
response = query_engine.query("What subclasses are available to the Monk class?") #4
print(response) #5

