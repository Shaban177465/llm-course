import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# عنوان الصفحة
st.title("🤖 AI Chatbot")
st.caption("بيتذكر المحادثة كاملة")

# نحفظ تاريخ المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# نعرض المحادثة القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# صندوق الكتابة
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    
    # نضيف رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # نبعت للـ AI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "أنت مساعد ذكي بتساعد في أي سؤال."}
        ] + st.session_state.messages,
        temperature=0.7
    )

    answer = response.choices[0].message.content

    # نضيف رد الـ AI
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)