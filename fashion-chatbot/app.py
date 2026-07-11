import streamlit as st
import json
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# تحميل المنتجات
import os
base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, "products.json"), "r") as f:
    products_data = json.load(f)

products_text = json.dumps(products_data, indent=2)

# واجهة الموقع
st.title("👗 Fashion Store Chatbot")
st.caption("Ask me anything about our products!")

# تاريخ المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# صندوق السؤال
if prompt := st.chat_input("Ask about products, sizes, prices..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # رد الـ AI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful fashion store assistant.
Answer customer questions based ONLY on our product catalog below.
Rules:
- If customer mentions a budget, show ONLY products within that budget
- If customer asks for a size, show ONLY products with that size available
- If a product is out of stock, mention it clearly
- Always mention price, available sizes, and colors
- If asked for an outfit, suggest matching products from the catalog
- Be friendly and helpful

Our Product Catalog:
{products_text}"""
            }
        ] + st.session_state.messages,
        temperature=0.7
    )

    answer = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)