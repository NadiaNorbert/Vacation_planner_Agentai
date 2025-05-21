import streamlit as st
from c1.gsearch import Tripplan  

st.set_page_config(page_title="Vacation Planner Chatbot", page_icon="🌍")
st.title("🌍 Vacation Planner Chatbot")

st.write(
    "Welcome to the Vacation Planner Chatbot! 🌟\n"
    "This chatbot will help you plan your dream vacation. Just provide the destination, number of days, and your budget, and let the magic happen! ✈️"
)

destination = st.text_input("Enter your destination here:", placeholder="e.g. Paris")
days = st.text_input("Enter the number of days here:", placeholder="e.g. 5")
budget = st.text_input("Enter your budget here:", placeholder="e.g. 10000")

if destination and days and budget:
    user_input = f"I want to go to {destination} for {days} days with a budget of {budget}. Can you help me plan my trip?"
    st.session_state.user_input = user_input

    with st.spinner("Analyzing your query..."):
        response_container = st.empty()
        output_text = ""
        for chunk in Tripplan(user_input):
             content = chunk.content

        # Optional: Auto formatting tweaks
             content = content.replace("Day", "📅 Day") 
             content = content.replace("Budget Breakdown", "💰 Budget Breakdown")
             content = content.replace("Flight Options", "✈️ Flight Options")
             content = content.replace("Tips and Recommendations", "📝 Tips and Recommendations")

        # Append and display
             output_text += content
             response_container.markdown(output_text, unsafe_allow_html=True)
        st.success("Here is your trip plan! 🎉")