## ✨ Automated MCQ Generator from PDF and Text Documents :

A web application built with Flask that extracts text from PDF, DOCX, and TXT files to generate multiple-choice questions (MCQs) using a generative AI model.

---

## 📚 Overview

This project allows users to:

Upload documents (PDF, DOCX, TXT)

Extract text from the uploaded file

Generate MCQs using an AI model (Google Gemini API)

Download the generated MCQs in TXT or PDF format

Ideal for educators, students, and content creators looking to automate question generation.

---

## 📂 Features

📚 Supports Multiple File Types: Extracts text from PDF, DOCX, and TXT files.

🤖 AI-Powered MCQ Generation: Uses Google Gemini AI for question creation.

📄 Downloadable Output: Save results as TXT or PDF.

🔍 Secure File Handling: Ensures safe uploads with file extension checks.

🚶 Web Interface: Simple and interactive UI using Flask and HTML templates.

---

## 🚀 Installation & Usage

### 📦 Requirements

Python 3.x

Flask

pdfplumber

python-docx

scikit-learn

FPDF

Google Generative AI SDK

## ⚖️ Setup

Clone the repository:

git clone https://github.com/your-repo/flask-mcq-generator.git
cd flask-mcq-generator

Install dependencies:

pip install -r requirements.txt

Set up your Google API Key:

export GOOGLE_API_KEY='your_api_key_here'

Run the application:

python app.py

Open your browser and navigate to:

http://127.0.0.1:5000/

---

## 💡 How It Works

Upload File: The user selects and uploads a document.

Text Extraction: The system extracts text from the file.

AI Processing: The extracted text is processed using the Google Gemini AI model to generate MCQs.

Results Display: The generated MCQs are displayed on a webpage.

Download Options: Users can download the MCQs as a TXT or PDF file.

---

## 📈 Example Output

## MCQ
Question: What is the primary function of data science?

A) Data Storage

B) Data Analysis

C) Web Development

D) UI Design

Correct Answer: B

---
## 💼 Future Enhancements

🔎 Enhanced AI Model: Improve question generation with better contextual understanding.

🌐 Multilingual Support: Enable MCQ generation in different languages.

💻 Web UI Upgrade: Develop a modern frontend using React or Vue.js.

🛠 Database Integration: Store user-generated questions for later retrieval.

## 🚀 Stay tuned for more updates!
