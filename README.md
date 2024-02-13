# primus_rag
A RAG system that hopefully will prove useful to people who play Dungeons & Dragons 5th edition.
This project is under active development and will change frequently.

###Files:
main.py - reads in the context files, creates, embeddings, and stores the vector index
ui.py - loads the vector index and generates a simple web interface for querying the context and recieving responses.

###Additional Notes:
The majority of work for this project has gone into obtaining the context data.  Intially, that code was contained within the same repo as the rag system itself.
I've since separated that code into https://github.com/rtjohn/fandom_etl.  However, the separation is not 100% complete and there may be some unecessary code in this repo still.

###TO DO:
1. Speed up response generation
2. Add additional context
3. Develop QC tests and evaluators
