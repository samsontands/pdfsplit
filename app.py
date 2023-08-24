import os
import PyPDF2
import streamlit as st
import io

# Initialize the counter in session state
if 'split_counter' not in st.session_state:
    st.session_state.split_counter = 0

def split_pdf(pdf_file, start_page, end_page):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages_total = len(pdf_reader.pages)

    if start_page < 1 or end_page > num_pages_total or start_page > end_page:
        return None

    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(start_page, end_page + 1):
        pdf_writer.add_page(pdf_reader.pages[page_num - 1])

    output_stream = io.BytesIO()
    pdf_writer.write(output_stream)
    output_stream.seek(0)  # Reset stream position to the beginning
    st.session_state.split_counter += 1  # Increment the counter
    return output_stream.read()

# Streamlit app
st.title("PDF Splitter")

# Display the counter
st.write(f"Split operations completed: {st.session_state.split_counter}")

# Create the file uploader
input_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if input_file is not None:
    # Create the input fields
    st.write("Specify page range:")
    start_page = st.number_input("Starting page number:", min_value=1, value=1)
    end_page = st.number_input("Ending page number:", min_value=start_page, value=start_page)

    # Create the button to initiate the PDF split
    if st.button("Split PDF"):
        output_pdf = split_pdf(input_file, start_page, end_page)
        if output_pdf is not None:
            st.success("PDF split operation complete!")
            st.download_button(
                label="Download Split PDF",
                data=output_pdf,
                file_name=f"split_pages_{start_page}-{end_page}.pdf",
                key="download_button"
            )

# Display instructions
st.write("Upload a PDF file, specify starting and ending page numbers, and click 'Split PDF'.")
