import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import PyPDF2

load_dotenv()
# initialize the LLM
llm = ChatOpenAI(api_key = os.getenv("OpenAI_API_KEY"), temperature=0.3, model="gpt-3.5-turbo")

# define the prompt template
COVER_LETTER_PROMPT = PromptTemplate(
    input_variable=["resume_text","job_title","company_name","job_description"],
    template="""
    You are an expert career coach and writer. 
    Using the following resume text, job title, company name, and job description, draft a tailored cover letter:
    
    Job Title: {job_title}
    Company Name: {company_name}
    
    use the following job description to understand the role:
    {job_description} 
    
    Keep the tone formal and professional, but friendly. Highlight relevant experience and ethusiasm for the role.
    """
)   

#create the chain
chain = LLMChain(llm=llm, prompt=COVER_LETTER_PROMPT)

# streamlit app
st.title("Cover Letter Generator")

uploaded_file = st.file_uploader("Upload your resume (PDF or txt)", type=["pdf","txt","docx"])
job_title = st.text_input("Job Title (e.g., Software Engineer):")
company_name = st.text_input("Company Name (optional):")
job_description = st.text_area("Job Description:", height=200)  

if st.button("Generate Cover Letter"):
    if not uploaded_file or job_title.strip() == ""  or job_description.strip() == "":
        st.warning("Please provide all inputs: resume, job title, company name, and job description.")
    else:
        with st.spinner("Generating cover letter..."):
            # Extract text from uploaded resume
            if uploaded_file.type == "application/pdf":
                reader = PyPDF2.PdfReader(uploaded_file)
                resume_text = ""
                for page in reader.pages:
                    resume_text += page.extract_text()
            elif uploaded_file.type == "text/plain":
                resume_text = str(uploaded_file.read(), "utf-8")
            else:
                st.error("Unsupported file type. Please upload a PDF or txt file.")
                resume_text = ""    
                
            
            # Generate cover letter
            cover_letter = chain.run(
                resume_text=resume_text,
                job_title=job_title,
                company_name=company_name,
                job_description=job_description
            )
        st.subheader("Generated Cover Letter:")
        st.text_area("Cover Letter:", value=cover_letter, height=300)