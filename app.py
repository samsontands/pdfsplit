import os
import PyPDF2
import streamlit as st

# Initialize the counter in session state
if 'counter' not in st.session_state:
    st.session_state.counter = 0

def split_pdf(pdf_file, output_folder, start_page, num_pages):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages_total = len(pdf_reader.pages)

    end_page = start_page + num_pages - 1

    if start_page < 1 or end_page > num_pages_total:
        return "Invalid page range."

    output_filename = f"output_pages_{start_page}-{end_page}.pdf"
    output_path = os.path.join(output_folder, output_filename)

    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(start_page, end_page + 1):
        pdf_writer.add_page(pdf_reader.pages[page_num - 1])

    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    # Update the counter
    st.session_state.counter += 1

    return f"Pages {start_page} to {end_page} have been split to {output_folder}. Splits done: {st.session_state.counter}"

# Streamlit app
st.title("PDF Splitter")

# Create the input fields
start_page = st.number_input("Starting page number:", min_value=1, value=1)
num_pages = st.number_input("Number of pages:", min_value=1, value=1)

# Create the file uploader
input_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Create the button to initiate the PDF split
if st.button("Split PDF"):
    if input_file is not None:
        output_folder = st.text_input("Output folder:", value="output")
        os.makedirs(output_folder, exist_ok=True)
        
        result = split_pdf(input_file, output_folder, start_page, num_pages)
        st.write(result)

# Display the counter
st.write(f"Total splits done: {st.session_state.counter}")

# Display instructions
st.write("Please upload a PDF file and provide page range inputs.")
