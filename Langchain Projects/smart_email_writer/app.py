import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
# initialize the LLM
llm = ChatOpenAI(api_key = os.getenv("OpenAI_API_KEY"), temperature=0.5, model="gpt-3.5-turbo")
# define the prompt template
prompt = PromptTemplate(
    input_variables=["bullet_points"],
    template="""
    You are an expert email writer. Using the following bullet points, draft a professional, friendly and concise email:
    {bullet_points}
    Ensure the email has a clear subject line, greeting, body, and closing.
    """
)

# create the chain
chain = LLMChain(llm=llm, prompt=prompt)

# streamlit app
st.title("Smart Email Writer with LangChain and OpenAI")    
st.write("Enter bullet points to generate a professional email.")
bullet_points = st.text_area("Enter bullet points for the email:", height=200)

if st.button("Generate Email"):
    if bullet_points.strip() == "":
        st.warning("Please enter some bullet points")
    else:
        with st.spinner("Generating email..."):
            email = chain.run(bullet_points=bullet_points)
        st.subheader("Drafted Email:")
        st.code(email, language='markdown')