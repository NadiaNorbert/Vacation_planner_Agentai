from agno.agent import Agent
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.ollama import Ollama
import streamlit as st
#from streamtrip import user_input
#from main import mood_finder
#import openai
#from multi_agent import mood_finder
def Tripplan(prompt: str):
    agent = Agent(
        name="google search agent",
        tools=[GoogleSearchTools()],
        description="You are a vacation planner guide.",
        instructions = [
        "You are a smart and friendly vacation planner assistant.",
        "You are a expert in creating a day-wise travel itinerary based on the user's travel dates and places."
        "When the user mentions a destination, suggest the top attractions and must-visit places there.",
        "Recommend the best time of year to visit the destination, considering weather and local events.",
        "Suggest popular and highly rated restaurants and local food experiences.",
        "Provide information about flight options, estimated costs, and an overall travel budget.",
        "Make all your suggestions in English.",
        "Metion the cost  in rupees and the currency of the country.",
        "Be proactive—if the user doesn't mention details like dates or interests."
        ],
        show_tool_calls=True,
        debug_mode=True,
        model=Ollama(id="llama3.2:1b"),
        )
   
    result=agent.run(prompt ,stream=True,markdown=True)  
    for partial_result in result:
         yield partial_result
    response_container = st.empty()
    output_text = ""
    for chunk in partial_result:
        content = chunk.content

        content = content.replace("Day", "📅 Day") 
        content = content.replace("Budget Breakdown", "💰 Budget Breakdown")
        content = content.replace("Flight Options", "✈️ Flight Options")
        content = content.replace("Tips and Recommendations", "📝 Tips and Recommendations")

        output_text += content
        response_container.markdown(output_text, unsafe_allow_html=True)

    

#Tripplan(prompt="Plan a trip to Paris for 5 days with a budget of 1000 euros.")  
    #return result
#promptt=input("Enter the prompt: ")

