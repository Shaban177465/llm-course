import json
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_completion(prompt, system="أنت مساعد مفيد", model="gpt-4o-mini", temperature=0.7):
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

def clean_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()

def generate_video_ideas(topic, count=3):
    result = get_completion(
        system="You are a helpful assistant that responds only in valid JSON. No extra text.",
        prompt=f"""
Generate {count} YouTube video ideas for an Arabic science channel called "فى 8 دقائق" about: {topic}

Rules:
- Each video is exactly 8 minutes
- Mix science with Quran verses
- Arabic Muslim audience

Respond with valid JSON only:
{{
  "ideas": [
    {{
      "title": "عنوان الفيديو",
      "hook": "أول جملة تجذب المشاهد",
      "quran_angle": "آية أو فكرة قرآنية مرتبطة"
    }}
  ]
}}
"""
    )

    print("=== الرد الخام ===")
    print(result)
    print("==================")

    cleaned = clean_json(result)
    data = json.loads(cleaned)
    return data["ideas"]

# تجربة
ideas = generate_video_ideas("الثقوب السوداء")

for i, idea in enumerate(ideas, 1):
    print(f"\nفكرة {i}:")
    print(f"العنوان: {idea['title']}")
    print(f"الهوك: {idea['hook']}")
    print(f"الزاوية القرآنية: {idea['quran_angle']}")
    print("---")