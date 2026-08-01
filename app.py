import streamlit as st

st.set_page_config(
    page_title="Skill Spark",                                              #Set browser tab title ,icon and layout.
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 Skill Spark")                                    #Big heading on the page.
st.subheader("Discover skills you should learn based on your hobbies!")

st.markdown("""                                                          
### How it works:
1. 📝 Go to **Hobby Input** page and enter your hobbies
2. 🤖 Our AI analyzes them
3. 🎓 Get personalized skill recommendations
4. 📚 Explore each skill in detail
5. 💾 Save your results for future reference
""")                                                                      #To write formatted text.

st.info("👈 Use the sidebar to navigate between pages")                  #Shows a blue info box.

st.markdown("---")                                                        #Draw a horizontal line to seperate the sections.
st.markdown("Built with ❤️ using Streamlit + OpenAI")                    #In markdown what you pass inside it decides what appears on screen
                                                                         #Markdown supports emojis and styling.