from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
from process import process
import streamlit as st

# from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
# import json


def ask(dir, file, user_question):
    data = process(dir, file)
    # print(json.dumps(data, indent=2))

    text = "Content:\n"
    if "content" in data:
        for element in data["content"]:
            text += element["text"]
            text += "\n"
    text += "\n\nTables:\n"

    # split into chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, separator=".", length_function=len
    )
    chunks = text_splitter.split_text(text)
    total_len = 0
    for chunk in chunks:
        total_len += len(chunk)

    if "tables" in data:
        for table in data["tables"]:
            chunks.append(table)
    # print(json.dumps(chunks, indent=2))

    def spend_money():
        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        if user_question:
            docs = knowledge_base.similarity_search(user_question)

            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
                print(cb)
                print(response)
                st.write(response)

    spend_money()


load_dotenv()
st.set_page_config(page_title="Ask your PDF")
st.header("Ask your PDF 💬")

dir = st.text_input("Enter the directory for your PDFs:")
file_path = st.text_input("Enter the filename to your PDF:")
user_question = st.text_input("Ask a question about your PDF:")
if dir and user_question and file_path:
    ask(dir, file_path, user_question)
