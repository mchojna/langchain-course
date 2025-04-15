import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

if __name__ == "__main__":
    print("Ingestion")
    loader = TextLoader("data/mediumblog.txt")
    document = loader.load()

    print("Splitting...")
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
    )
    texts = text_splitter.split_documents(document)
    print(f"Splitted into {len(texts)} chunks")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002", api_key=os.getenv("OPENAI_API_KEY")
    )

    print("Ingesting...")
    PineconeVectorStore.from_documents(
        documents=texts, embedding=embeddings, index_name=os.getenv("INDEX_NAME")
    )
    print("Finished")
