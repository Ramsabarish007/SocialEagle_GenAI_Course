import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import PyPDF2

load_dotenv()

# initialize the LLM
llm = ChatOpenAI(api_key=os.getenv("OpenAI_API_KEY"), temperature=0.3, model="gpt-3.5-turbo")

#prompt template for mock interview questions
MOCK_INTERVIEW_PROMPT = PromptTemplate(
    input_variable=["role","job_description"],
    template="""
    You are an expert career coach. Based on the following resume text, and job description, generate a list of 5 **technical** interview questions that a candidate might be asked for this role.
    
    only include questions that test technical skillsets, knowledge, and problem-solving abilities relevant to the job description.
    do Not include situational or behavioral questions.
    
    for each question, provide a clear, strong sample answer that a well-prepared candidate might give.
    
    Number them 1 to 5, and format like this:
    1. Question: [Interview Question]
       Sample Answer: [Strong Sample Answer]
    
    Provide the questions in a numbered list format.
    """
)

# create the chain
chain = LLMChain(llm=llm, prompt=MOCK_INTERVIEW_PROMPT)

# streamlit app
st.title("Mock Interview Question Generator")   

role = st.text_input("Enter the role you're applying for:") 
job_description = st.text_area("Job Description (paste here):", height=200)

if st.button("Generate Mock Interview Questions"):
    if role.strip() == "" or job_description.strip() == "":
        st.warning("Please provide both the role and job description.")
    else:
        with st.spinner("Generating mock interview questions..."):
            # Generate mock interview questions
            interview_questions = chain.run(role=role, job_description=job_description)
            st.subheader("Mock Interview Questions and Sample Answers")
            st.text(interview_questions)