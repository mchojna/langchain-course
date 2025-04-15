import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub

load_dotenv()

if __name__ == "__main__":
    pdf_path = "data/2210.03629v3.pdf"
    loader = PyPDFLoader(file_path=pdf_path)
    document = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=30,
        separator="\n",
    )

    docs = text_splitter.split_documents(documents=document)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002", api_key=os.getenv("OPENAI_API_KEY")
    )

    # vector_store = FAISS.from_documents(docs, embeddings)
    # vector_store.save_local("data/faiss_index_react")

    vector_store = FAISS.load_local(
        folder_path="data/faiss_index_react",
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(
        OpenAI(), retrieval_qa_chat_prompt
    )
    retrieval_chain = create_retrieval_chain(
        vector_store.as_retriever(), combine_docs_chain
    )
    result = retrieval_chain.invoke({"input": "What is React?"})
    print(result["answer"])
