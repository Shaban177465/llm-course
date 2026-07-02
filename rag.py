from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# 1. اقرأ الملف
with open("test.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2. قطّع النص لأجزاء صغيرة
splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.create_documents([text])
print(f"عدد الأجزاء: {len(chunks)}")

# 3. حوّل الأجزاء لـ Embeddings واحفظها
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever()

# 4. اعمل الـ Prompt
prompt = ChatPromptTemplate.from_template("""
أجب على السؤال بناءً على السياق التالي فقط:

السياق: {context}

السؤال: {question}
""")

# 5. اعمل الـ Chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 6. اسأل
questions = [
    "مين مؤسس القناة؟",
    "إيه هدف القناة؟",
    "إيه الموضوعات اللي بتغطيها القناة؟"
]

for q in questions:
    answer = chain.invoke(q)
    print(f"\nسؤال: {q}")
    print(f"جواب: {answer}")