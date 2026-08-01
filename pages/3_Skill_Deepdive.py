import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ai.recommender import get_recommendations

st.title("🔍 Skill Deep Dive")

if "recommendations" not in st.session_state:
    st.warning("Please generate recommendations first!")
    st.stop()

st.write("Enter a skill to explore in detail:")
skill = st.text_input("Skill name", placeholder="e.g. Data Analysis")

if st.button("🔎 Explore Skill"):
    if skill.strip() == "":
        st.warning("Please enter a skill name!")
    else:
        with st.spinner("Fetching details..."):
            prompt = f"Give a detailed learning path for {skill}. Include: 1) What it is 2) Why it's valuable 3) Step by step learning path 4) Top 3 free resources 5) Time to learn"
            from ai.recommender import get_recommendations
            import requests
            from dotenv import load_dotenv
            load_dotenv()
            HF_TOKEN = os.getenv("HF_TOKEN")
            API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"
            headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
            payload = {"model": "meta-llama/llama-3.1-8b-instruct", "messages": [{"role": "user", "content": prompt}], "max_tokens": 600}
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
                st.markdown(result)
            else:
                st.error("Error fetching details!")