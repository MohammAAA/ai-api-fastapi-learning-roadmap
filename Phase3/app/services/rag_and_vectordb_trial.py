import os
import uuid # to assign unique IDs to the files 
import tempfile # to create temp files from uploaded files
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from openai import OpenAI, RateLimitError
import logging
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from qdrant_client import QdrantClient # Local Vector database
from langchain_qdrant import QdrantVectorStore


COLLECTION = "docs_chunks"
QDRANT_URL = "http://localhost:6333"


app = FastAPI()
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client_qdrant = QdrantClient(QDRANT_URL) # Initialize the Qdrant client


raw_files = {} # Stores file name and byte-content (in-memory) in case we need them after the uploaded temp file is deleted
docs_store = {} # Stores the parsed file content (eg.: PDF, MD, CSV, ...) 

def load_file_with_langchain(tmp_path: str, filename: str):
    '''“loading” means: read each file → extract its text (and metadata like filename/page/row) → convert into a consistent internal format (often a list of Document objects)''' 
    file_extension = os.path.splitext(filename.lower())[1] # Get the file extension

    if file_extension == ".pdf":
        return PyPDFLoader(tmp_path).load()
    if file_extension in (".txt", ".md"):
        return TextLoader(tmp_path, encoding="utf-8").load()
    if file_extension == ".csv":
        return CSVLoader(file_path=tmp_path).load()

    raise ValueError(f"Unsupported extension: {file_extension}")

# 1- This function will be used as a dependancy injection (DI)
# where we define “lightweightprovider functions” (factories) that create or return shared objects,
# and then inject them into endpoints by adding parameters declared with "Depends()""
# 2- The function (get_vectorstore()) will depend on this function 
def get_embeddings():
    '''
    Embedding:
    Embedding models transform raw text—such as a sentence, paragraph, or tweet into a fixed-length vector of numbers that captures its semantic meaning.
    These vectors allow machines to compare and search text based on meaning rather than exact words.
    In practice, this means that texts with similar ideas are placed close together in the vector space.
    For example, instead of matching only the phrase “machine learning”, embeddings can surface documents that discuss related concepts even when different wording is used.
    '''
    return FastEmbedEmbeddings()

# DI to the endpoint: GET (/query)
def get_vectorstore(embeddings: FastEmbedEmbeddings = Depends(get_embeddings)):
    # Reconnect to the already-created collection (no re-indexing)
    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=COLLECTION,
        url=QDRANT_URL,
    )

@app.post("/upload")
async def upload_document(document_file: UploadFile = File(..., description="The document file to be uploaded")):
    file_bytes = await document_file.read() # Reads the uploaded file into memory
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Error, empty file")
    
    file_id = str(uuid.uuid4()) # We use UUID4 because it generates a random UUID, unlike UUID1 which uses the computer network address so it may compromise privacy

    # Store raw bytes in memory
    raw_files[file_id] = {
        "filename": document_file.filename,
        "content_type": document_file.content_type,
        "bytes": file_bytes,
    }

    # Save to a temp file so LangChain loaders can read via the temp file's path
    with tempfile.NamedTemporaryFile(delete=False) as tmp: # use (delete = False) because we don't want the temp file to be deleted at the end of the (with) block, we want to load it first in the (try) block
        tmp.write(file_bytes) # Write the uploaded file to a real tmp file on disk
        tmp_path = tmp.name # tempfile.NamedTemporaryFile(...): creates a temporary file that has an actual filesystem path available as tmp.name

    try:
        # Load the uploaded document
        docs = load_file_with_langchain(tmp_path, document_file.filename)
    finally:
        os.remove(tmp_path) # remove the temp file

    docs_store[file_id] = docs # store the parsed content

    # Chunking the loaded document
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=50) # The recursive chunk trying to keep all paragraphs (and then sentences, and then words) together as long as possible, as those would generically seem to be the strongest semantically related pieces of text.
    texts = text_splitter.split_documents(docs)

    embeddings = get_embeddings()
# The following line can be used to embed the chunks in case we don't want to use langchain
    # docs_vectors = embeddings.embed_documents([doc.page_content for doc in texts])

    # Store the embeddings of all the chunks in the Qdrant vector DB
    try:
        vectorstore = QdrantVectorStore.from_documents(
            documents=texts,                 # our chunk Documents
            embedding=embeddings,             # OpenAIEmbeddings(...), it will call the previously commented embeddings.embed_documents()
            url=QDRANT_URL,    # The Qdrant URL and port number
            collection_name=COLLECTION  
        )

    except RateLimitError:
        raise HTTPException(status_code=429, detail="OpenAI quota exceeded (insufficient_quota)")
    return {
        "file_id": file_id,
        "filename": document_file.filename,
        "documents_loaded": len(docs),
    }

@app.get("/query")
def query_handler (query: str, vector_store: QdrantVectorStore = Depends(get_vectorstore)):
    query_result = vector_store.similarity_search(query, k=5) # return the most similar 5 search results
    return [{"similarity_search_text": d.page_content, "metadata": d.metadata} for d in query_result]

@app.post("/ask_ai")
async def ask_question(question: str, vector_store: QdrantVectorStore = Depends(get_vectorstore)):
    query_result = vector_store.similarity_search(question, k=5)
    try:
        prompt = f"Answer the following question '''{question}''' \n\n based on the following context: '''{query_result}''' \n\n"
        response = client_openai.responses.create(
            model="gpt-4o-mini",
            input=prompt,
            temperature=1.0,
        )
        return {
            "answer": response.output_text,
            "tokens": response.usage.total_tokens,
            "model": response.model
        }
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except Exception as e:
        logging.error(f"API error: {e}") # Internal loggings for debugging purposes, the user does not have access to it.
        raise HTTPException(status_code=500, detail="Internal server error")
