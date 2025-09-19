from flask import Flask, request, render_template, send_file
import PyPDF2
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
import re
from werkzeug.utils import secure_filename

application = Flask(__name__)
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/generate', methods=['POST'])
def generate_wordcloud():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    
    if file and file.filename.lower().endswith('.pdf'):
        # Read PDF
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Clean and filter text
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        filtered_text = ' '.join([word for word in words if word not in stop_words and len(word) > 2])
        
        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)
        
        # Convert to base64 for display
        img = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(img, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        img.seek(0)
        
        img_b64 = base64.b64encode(img.getvalue()).decode()
        
        return render_template('result.html', image=img_b64)
    
    return 'Invalid file type. Please upload a PDF file.', 400

if __name__ == '__main__':
    application.run(debug=True)