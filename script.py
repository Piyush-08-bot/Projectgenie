# ######## cohere ##########

import streamlit as st
import cohere
import fitz  # PyMuPDF
import pdfplumber
import re

# try:
#     import fitz  
#     pymupdf_available = True
# except ImportError:
#     pymupdf_available = False
    
# try:
#     import pdfplumber
#     pdfplumber_available = True
# except ImportError:
#     pdfplumber_available = False

st.set_page_config(layout="wide")  
st.title("🚀 Project Genie & Resume Analyzer")



def parse_resume(text):
    """Extracts key details like name, education, skills, and experience from resume text."""
    name = re.findall(r"Name:\s*(.*)", text)
    education = re.findall(r"Education:\s*(.*)", text)
    skills = re.findall(r"Skills:\s*(.*)", text)
    experience = re.findall(r"Experience:\s*(.*)", text)
    interests = re.findall(r"Interests:\s*(.*)", text)

    return {
        "name": name[0] if name else "N/A",
        "education": education if education else ["N/A"],
        "skills": skills[0].split(", ") if skills else ["N/A"],
        "experience": experience if experience else ["N/A"],
        "interests": interests[0].split(", ") if interests else ["N/A"]
    }
    

def initialize_cohere():
    api_keys = [st.secrets["api_keys"].get("API_KEY_1"), st.secrets["api_keys"].get("API_KEY_2"), st.secrets["api_keys"].get("API_KEY_3")]
    for key in api_keys:
        if key:
            try:
                co = cohere.Client(key)
                return co
            except Exception:
                continue
    st.error("🚨 All API keys failed. APIs not working.")
    return None

co = initialize_cohere()


col1, col2 = st.columns([1, 1])

with col1:
  
    st.header("📄 Resume Analyzer")
    uploaded_file = st.file_uploader("Upload your PDF Resume", type="pdf")
    
    def extract_text_pymupdf(uploaded_file):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        return text
    
    def extract_text_pdfplumber(uploaded_file):
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        return text
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        method = st.radio("Choose Extraction Method", ["PyMuPDF", "pdfplumber"])
        
     
        # resume_text = extract_text_pymupdf(uploaded_file) if method == "PyMuPDF" else extract_text_pdfplumber(uploaded_file)
        
        st.subheader("Extracted Resume Text")
        st.text_area("", resume_text, height=300)

        resume_text = extract_text_pymupdf(uploaded_file) if method == "PyMuPDF" else extract_text_pdfplumber(uploaded_file)
        parsed_data = parse_resume(resume_text)  # Extract structured data


        
        st.subheader("Anything you want to learn while building these projects?")
        user_learning_input = st.text_input("")
        
        if st.button("Generate Project Ideas"):
            st.session_state.resume_text = resume_text 
            st.session_state.user_learning_input = user_learning_input 
            st.session_state.button_clicked = True 

with col2:
    # Generate the AI prompt with parsed data
    prompt = f"""You are an AI project advisor helping students build relevant and achievable projects.

### **Student Profile:**
- **Name**: {parsed_data['name']}
- **Education**: {', '.join(parsed_data['education'])}
- **Skills**: {', '.join(parsed_data['skills'])}
- **Experience**: {', '.join(parsed_data['experience'])}
- **Interests**: {', '.join(parsed_data['interests'])}

### **Project Guidelines:**
1. Use only the technologies mentioned in skills.
2. Suggest 3 projects—one beginner, one intermediate, and one advanced.
3. Projects should be achievable within 2-6 weeks.
4. Align projects with career trends.
5. Format output as follows:

#### **Project {1/2/3}: [Project Title]**
- **Level**: Beginner/Intermediate/Advanced  
- **Description**: [Brief overview]  
- **Step-by-step Roadmap**:  
  - Step 1: …  
  - Step 2: …  
  - Step 3: …  
- **Required Resources**: [Courses, GitHub repos, docs, or tutorials]  
- **Expected Outcome**: [What the student will learn]  

Only return structured project ideas. No extra explanations.
"""
        
    
    try:
        response = co.generate(
            model="command-r-08-2024",
            prompt=prompt,
            max_tokens=700
        )
        st.subheader("Recommended Project Ideas:")
        st.write(response.generations[0].text)
    except Exception as e:
        st.error(f"🚨 Error generating project ideas: {str(e)}")
        
       
    st.markdown("---")
    st.subheader("💡 Tips for Effective Learning")
    st.write("- Break projects into smaller tasks and set milestones.")
    st.write("- Follow the recommended resources step by step.")
    st.write("- Document your learning journey through blogs or GitHub.")



# import streamlit as st
# import cohere


# api_key = st.secrets["api_keys"]["API_KEY"]

# # # Initialize Cohere client
# co = cohere.Client(api_key)


# # Streamlit interface
# st.title("Project Genie Chatbot")
# st.write("Enter your interests to get project ideas.")

# user_input = st.text_input("Enter your interests:")

# if user_input:
#     prompt = f"Suggest a unique project idea based on the following interests: {user_input}"
    
#     response = co.generate(
#         model="command-r-08-2024",
#         prompt=prompt,
#         max_tokens=5
#     )
    
#     st.write("Generated Project Idea:")
#     st.write(response.generations[0].text)
    
    
    
# import streamlit as st
# import fitz  # PyMuPDF
# import pdfplumber

# # Function to extract text using PyMuPDF
# def extract_text_pymupdf(uploaded_file):
#     doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
#     text = "\n".join(page.get_text() for page in doc)
#     return text

# # Function to extract text using pdfplumber (alternative)
# def extract_text_pdfplumber(uploaded_file):
#     with pdfplumber.open(uploaded_file) as pdf:
#         text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
#     return text

# # Streamlit UI
# st.title("📄 Resume Analyzer")

# uploaded_file = st.file_uploader("Upload your PDF Resume", type="pdf")

# if uploaded_file is not None:
#     st.success("File uploaded successfully!")
    
#     # Choose extraction method
#     method = st.radio("Choose Extraction Method", ["PyMuPDF", "pdfplumber"])

#     # Extract text
#     if method == "PyMuPDF":
#         resume_text = extract_text_pymupdf(uploaded_file)
#     else:
#         resume_text = extract_text_pdfplumber(uploaded_file)

#     # Display extracted text
#     st.subheader("Extracted Resume Text")
#     st.text_area("", resume_text, height=300)

#     # Option to process further
#     if st.button("Analyze Resume"):
#         st.write("🔍 **Processing for project recommendations...**")
#         # You can now pass `resume_text` to your LLM for project suggestions!









# import streamlit as st
# from llama_cpp import Llama

# # Initialize Llama model
# llama_model = Llama(model_path="/Users/vedpawar/llama_models/mistral-7b-instruct")  # Replace with your model path

# # Define Streamlit app interface
# st.title("Llama 3.2 Chatbot")
# st.write("Enter a prompt, and Llama 3.2 will generate a response:")

# # Take user input
# user_input = st.text_input("Enter your prompt:")

# # Generate a response from Llama 3.2
# if user_input:
#     response = llama_model(user_input)  # Adjust based on the function used to query the model
#     st.write("Llama's Response:")
#     st.write(response)



# from transformers import GPT2LMHeadModel, GPT2Tokenizer

# model_name = "gpt2"
# model = GPT2LMHeadModel.from_pretrained(model_name)
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# input_text = "Once upon a time"
# inputs = tokenizer.encode(input_text, return_tensors="pt")
# outputs = model.generate(inputs, max_length=100, num_return_sequences=1)

# print(tokenizer.decode(outputs[0], skip_special_tokens=True))

