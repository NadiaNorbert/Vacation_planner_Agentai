from c1.chat import chat
from pydantic import BaseModel
from openai import OpenAI
from c1.gsearch import Tripplan

class Identifier(BaseModel):
    is_search: bool
    is_trip: bool

IDENTIFIER_PROMPT = """
You are an agent specialized in query classification.
Your task is to determine if the user's query requires a RAG search.
user_input: {user_input}
You are a vacation planner agent.
Guidelines:
- Classify as search true if the query is general knowledge (e.g. "Who is...", "What is...", "When did...","How is...")
- Classify as search if the query asks about facts, history, or current events
- Classify as Trip if they ask you to suggest vacation places to visit
- Classify as Trip if they ask you to create vacation plan for the place
- Classify as Trip if they ask you to suggest hotels to stay/accommodate
- Classify as Trip if they ask you to give route inside the vacation/trip place
- Classify as Trip if they ask you to check travelling tickets for travel
- Classify as Trip if they ask you to suggest best month/season to visit vacation places
Analyze the query and determine if it requires searching.
"""

def mood_finder(user_input: str):
  from openai import OpenAI
  
  client = OpenAI(base_url="your_url", api_key="your_apikey")
  
  response = client.beta.chat.completions.parse(
      model="openai/gpt-4o-mini",
      messages=[
        {
          'role': 'user',
          'content': user_input,
        }
      ],
      response_format=Identifier,
  )
  
  filtered_response = Identifier.model_validate_json(response.choices[0].message.content)
  return filtered_response

def main(user_input: str):
    identifier = mood_finder(IDENTIFIER_PROMPT.format(user_input=user_input))
    print(f"Identifier: {identifier}")

    if identifier.is_search:
        rag_response = chat(user_input)
        print(f"Search Response:\n{rag_response}")
        return rag_response

    if identifier.is_trip:
        trip_response = Tripplan(user_input=user_input)
        print(f"Trip Plan:\n{trip_response}")
        return trip_response

    return "Sorry, I couldn't classify your query."

