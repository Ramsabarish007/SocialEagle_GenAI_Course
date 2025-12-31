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
    input_variables=["code_task"],
    template="""
    You are a helpful coding assistant. Help the user with following task:
    {code_task}
    Provide clean, well-commented code and explanations if needed.
    """
)

chain = LLMChain(llm=llm, prompt=prompt)

# streamlit app
st.title("Code Assistant with LangChain and OpenAI")

code_task = st.text_area("Describe your coding task:", height=200)

if st.button("Generate Code"):
    if code_task.strip() == "":
        st.warning("Please enter a task description")
    else:
        with st.spinner("Generating code..."):
            response = chain.run(code_task=code_task)
        st.subheader("Assistant response:")
        st.code(response, language='python')