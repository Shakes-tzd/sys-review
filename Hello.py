import streamlit as st
import openai
import pandas as pd
import io
from PyPDF2 import PdfReader

# Function to read PDF file and convert it to text
def pdf_to_text(file_data):
    reader = PdfReader(file_data)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to send prompt to OpenAI and get response
def query_openai(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",  # You can update the model as needed
        prompt=prompt,
        temperature=0.5,
        max_tokens=500
    )
    return response.choices[0].text.strip()

# Streamlit App
def main():
    # Set up Streamlit page
    st.set_page_config(page_title="Systematic Review Assistant", page_icon="🔍")

    # OpenAI API key setup (ensure your API key is securely stored)
    openai.api_key = st.secrets["openai_api_key"]

    # Sidebar for file upload
    st.sidebar.title("Upload Article")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=['pdf', 'txt'])
    
    # Main area
    st.title("Systematic Review Assistant")
    st.markdown("## Full-Text Review and Data Extraction")

    # Process uploaded file
    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension == 'pdf':
            text_content = pdf_to_text(uploaded_file)
        elif file_extension == 'txt':
            text_content = uploaded_file.getvalue().decode("utf-8")
        else:
            st.error("Unsupported file format.")
            return

        # Display extracted text (optional)
        st.markdown("### Extracted Text")
        st.text_area("Content", text_content, height=300)

        # OpenAI Prompt
        prompt = f"Extract the following information from the article: 1) Number of patients in the study, 2) Average age of patients, 3) Minimum and maximum ages, 4) Time for facial reinnervation (min and max), 5) Follow-up duration.\n\n{text_content}"
        extracted_info = query_openai(prompt)

        # Display extracted information
        st.markdown("### Extracted Information")
        st.text_area("Extracted Data", extracted_info, height=150)

        # Confirmation button
        if st.button("Confirm Extracted Data"):
            # Processing confirmed data (e.g., saving to a DataFrame)
            st.success("Data confirmed and processed.")

    else:
        st.write("Please upload an article to proceed.")

if __name__ == "__main__":
    main()
