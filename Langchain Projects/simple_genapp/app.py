import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env
load_dotenv()

# Read API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY not found. "
        "Create a .env file and add your key."
    )

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=api_key
)

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("human", "Explain {topic} in simple terms.")
])

# Chain (LangChain Expression Language)
chain = prompt | llm

# Run app
if __name__ == "__main__":
    topic = input("Enter a topic to explain: ")
    response = chain.invoke({"topic": topic})
    print("\nAI says:\n")
    print(response.content)
