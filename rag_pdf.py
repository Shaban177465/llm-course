from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# 1. اقرأ الـ PDF
loader = PyPDFLoader("document.pdf")
pages = loader.load()
print(f"عدد الصفحات: {len(pages)}")

# 2. قطّع لأجزاء صغيرة
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(pages)
print(f"عدد الأجزاء: {len(chunks)}")

# 3. حوّل لـ Embeddings
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever()

# 4. الـ Prompt
prompt = ChatPromptTemplate.from_template("""
أجب على السؤال بناءً على السياق التالي فقط.
لو المعلومة مش موجودة قول "مش موجود في الملف".

السياق: {context}
السؤال: {question}
""")

# 5. الـ Chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 6. محادثة مع الـ PDF
print("\n=== اسأل عن الـ PDF — اكتب 'خروج' للخروج ===\n")

while True:
    question = input("سؤالك: ")
    if question == "خروج":
        break
    answer = chain.invoke(question)
    print(f"الجواب: {answer}\n")