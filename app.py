import os
from flask import Flask, render_template, request, send_file
import pdfplumber
import docx
import csv
from werkzeug.utils import secure_filename
import google.generativeai as genai
from fpdf import FPDF  # pip install fpdf

#Set your API Key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAqtUlUwuP_fe0nfT1he3qmKb6yJjhlLds'
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel("models/gemini-1.5-pro")

app = Flask(__name__, template_folder='../templates')
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULTS_FOLDER'] = 'results/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf','txt','docx'}

#---------------------Connect html
@app.route('/')
def index():
    return render_template('index.html')
#---------------------------------------------------------------------Func For GenMCQs
def allowed_file(filename):
    #rasel.pdf
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']




def extract_text_from_file(file_path):

    #rasel.pdf
    ext = file_path.rsplit(".",1)[1].lower()

    if ext == "pdf":
        with pdfplumber.open(file_path) as pdf:
            text =''.join([i.extract_text() for i in pdf.pages])
        return text

    elif ext == "docx":
        doc = docx.Document(file_path)
        text =''.join([i.text for i in doc.paragraphs])
        return text

    elif ext == "txt":
        with open(file_path,'r') as file:
            return file.read()
    return None


#---------------------------------------------------------LLMs Model Training

def Question_mcqs_generator(input_text, num_questions):
    prompt = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
    '{input_text}'
    Please generate {num_questions} MCQs from the text. Each question should have:
    - A clear question
    - Four answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    Format:
    ## MCQ
    Question: [question]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [correct option]
    """

    response = model.generate_content(prompt).text.strip()
    return response

#-----------------------------------------------prepare Text for LLMs Model
@app.route('/generate', methods=['POST'])
def generate_mcqs():
    if 'file' not in request.files:
        return "File Upload kor Mama Age"

    file = request.files['file']
    num_questions = request.form['num_questions']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        #pdf, txt, docx
        text = extract_text_from_file(file_path)

        if text:
            num_questions = int(request.form['num_questions'])
            mcqs = Question_mcqs_generator(text, num_questions)

            #return render_template('results.html',mcqs=mcqs) # If you  interest for only show results
#=============================================================Download in PDF pROGRESS bAR==================
            # Save the generated MCQs to a file
            txt_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.txt"
            pdf_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.pdf"
            save_mcqs_to_file(mcqs, txt_filename)
            create_pdf(mcqs, pdf_filename)

            # Display and allow downloading
            return render_template('results.html', mcqs=mcqs, txt_filename=txt_filename, pdf_filename=pdf_filename)
        return "Invalid file format"

def save_mcqs_to_file(mcqs, filename):
    results_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    with open(results_path, 'w') as f:
        f.write(mcqs)
    return results_path

def create_pdf(mcqs, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for mcq in mcqs.split("## MCQ"):
        if mcq.strip():
            pdf.multi_cell(0, 10, mcq.strip())
            pdf.ln(5)  # Add a line break

    pdf_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    pdf.output(pdf_path)
    return pdf_path
#--------------------------------------------------------Download As PDF route
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    if not os.path.exists(app.config['RESULTS_FOLDER']):
        os.makedirs(app.config['RESULTS_FOLDER'])
    app.run(debug=True)