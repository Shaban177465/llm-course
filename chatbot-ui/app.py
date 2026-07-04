import streamlit as st
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import tempfile
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

st.title("📄 PDF Chatbot")
st.caption("ارفع أي PDF واسأل عنه")

# رفع الـ PDF
uploaded_file = st.file_uploader("ارفع ملف PDF", type="pdf")

if uploaded_file:
    # نحفظه مؤقتاً
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(uploaded_file.read())
        tmp_path = f.name

    with st.spinner("بيقرأ الـ PDF..."):
        # نقرأ ونقسم
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50
        )
        chunks = splitter.split_documents(pages)

        # نعمل الـ RAG
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever()

        prompt = ChatPromptTemplate.from_template("""
أجب على السؤال من السياق فقط.
لو مش موجود قول "مش موجود في الملف".

السياق: {context}
السؤال: {question}
""")
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    st.success(f"✅ اتقرأ {len(pages)} صفحة — اسأل دلوقتي!")

    # صندوق السؤال
    question = st.chat_input("اسأل عن الـ PDF...")
    if question:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("بيفكر..."):
                answer = chain.invoke(question)
            st.write(answer)

    os.unlink(tmp_path)

else:
    st.info("👆 ارفع PDF عشان تبدأ")