from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chat(history, user_message, system="أنت مساعد مفيد"):
    # بنضيف رسالة المستخدم الجديدة للتاريخ
    history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system}] + history,
        temperature=0.7
    )

    # بناخد رد الموديل ونضيفه للتاريخ
    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})

    return assistant_message, history

# ================================
if __name__ == "__main__":
    print("=== Chatbot شغال — اكتب 'خروج' للخروج ===\n")

    history: list[dict[str, str]] = []
    system = "أنت مساعد ذكى لقناة يوتيوب علمية اسمها فى 8 دقائق. بتساعد في أفكار المحتوى."

    while True:
        user_input = input("أنت: ")

        if user_input == "خروج":
            print("مع السلامة!")
            break

        response, history = chat(history, user_input, system)
        print(f"البوت: {response}\n")