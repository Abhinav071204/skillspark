import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ai.recommender import get_recommendations

st.title("🎓 Skill Recommendations")

if "hobbies" not in st.session_state:
    st.warning("Please go to Hobby Input page first!")
    st.stop()

hobbies = st.session_state["hobbies"]
level = st.session_state["level"]
goal = st.session_state["goal"]

st.write(f"**Your hobbies:** {hobbies}")
st.write(f"**Level:** {level} | **Goal:** {goal}")
st.markdown("---")

if st.button("🤖 Generate Recommendations"):
    with st.spinner("AI is analyzing your hobbies..."):
        result = get_recommendations(hobbies, level, goal)
        st.session_state["recommendations"] = result
        st.markdown(result)