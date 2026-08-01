import streamlit as st

st.set_page_config(page_title="Hobby Input", page_icon="📝")                 

st.title("📝 Enter Your Hobbies")
st.write("Tell us what you love doing and we'll recommend skills for you!")

hobbies = st.text_area(
    "Enter your hobbies (one per line)",                                        #User can type multiple hobbies, placeholder is grey hint text.      
    placeholder="e.g.\nPlaying guitar\nReading books\nPlaying cricket"
)

level = st.selectbox(
    "Your current skill level",                                                #give a dropdown menu with options provided below in the code.
    ["Beginner", "Intermediate", "Advanced"]
)

goal = st.selectbox(
    "Your main goal",
    ["Get a job", "Personal growth", "Start a business", "Just curious"]
)

if st.button("🚀 Find My Skills"):                                            #creates a clickable button, everything inside if block runs when button is clicked.
    if hobbies.strip() == "":                                                 #To remove empty spaces. If text is empty it shows a warning message.
        st.warning("Please enter at least one hobby!")
    else:                                                                     #It's like a temporary memory, saves data so other pages can access them
        st.session_state["hobbies"] = hobbies
        st.session_state["level"] = level
        st.session_state["goal"] = goal
        st.success("✅ Hobbies saved! Go to Recommendations page.")          #Shows a green success msg when everything is saved.