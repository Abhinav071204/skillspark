import requests
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

def get_recommendations(hobbies, level, goal):
    API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    prompt = f"""You are a career skills advisor.

User hobbies: {hobbies}
Skill level: {level}
Goal: {goal}

Suggest exactly 5 skills. For each skill give:
1. Skill name
2. Why it suits their hobbies (1-2 lines)
3. One free resource with full URL (Coursera, YouTube, freeCodeCamp, Khan Academy etc)

Format exactly like this for each skill:
SKILL: [skill name]
WHY: [reason]
RESOURCE: [resource name] - [full URL starting with https://]

Do not add any extra text."""

    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"