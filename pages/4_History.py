import streamlit as st

st.title("💾 History")

if "hobbies" not in st.session_state:
    st.warning("No history yet! Go to Hobby Input page first.")
    st.stop()

st.subheader("Your Last Session")
st.write(f"**Hobbies:** {st.session_state.get('hobbies', 'N/A')}")
st.write(f"**Level:** {st.session_state.get('level', 'N/A')}")
st.write(f"**Goal:** {st.session_state.get('goal', 'N/A')}")

st.markdown("---")
st.subheader("Your Recommendations")

if "recommendations" in st.session_state:
    st.markdown(st.session_state["recommendations"])
else:
    st.info("No recommendations generated yet!")