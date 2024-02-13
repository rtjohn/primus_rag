# primus_rag
A RAG system that hopefully will prove useful to people who play Dungeons & Dragons 5th edition.
This project is under active development and will change frequently.

### Files:
main.py - reads in the context files, creates embeddings, and stores them in a vector index
ui.py - loads the vector index and generates a simple web interface for querying the context and getting back responses.

### Additional Notes:
The majority of work for this project has gone into obtaining the context data.  Intially, data collection code was contained within the same repo as the rag system itself.
I've since separated that code into https://github.com/rtjohn/fandom_etl.  However, the separation is not 100% complete and there may be some unecessary code in this repo still.

## TO DO:
1. Move all this code to an EC2 for public consumption
2. Speed up response generation
3. Add additional context
4. Develop QC tests and evaluators
