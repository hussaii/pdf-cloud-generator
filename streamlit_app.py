import streamlit as st
import PyPDF2
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="PDF Word Cloud Generator", page_icon="☁️")

st.title("☁️ PDF Word Cloud Generator")
st.write("Upload a PDF file to generate a word cloud with stop words removed")

stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Generating word cloud..."):
        # Read PDF
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        if text.strip():
            # Clean and filter text
            words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            filtered_text = ' '.join([word for word in words if word not in stop_words and len(word) > 2])
            
            if filtered_text:
                # Generate word cloud
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)
                
                # Display word cloud
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
                
                # Download button
                plt.savefig('wordcloud.png', dpi=300, bbox_inches='tight')
                with open('wordcloud.png', 'rb') as file:
                    st.download_button(
                        label="Download Word Cloud",
                        data=file.read(),
                        file_name="wordcloud.png",
                        mime="image/png"
                    )
            else:
                st.error("No valid text found after filtering")
        else:
            st.error("No text could be extracted from the PDF")