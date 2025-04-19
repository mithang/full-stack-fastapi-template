

from typing import Any

from fastapi import APIRouter, File, UploadFile
import requests
from pydantic import BaseModel
import fitz  # PyMuPDF

router = APIRouter(tags=["AI for Automation and Productivity"], prefix="/deepseek")


class ContentWriterInput(BaseModel):
    tone: str
    topic: str  # "Professional", "Casual", "Persuasive"
    keywords: str


class EmailContentInput(BaseModel):
    tone: str
    content: str = "Formal"  # "Formal", "Casual", "Friendly"


OLLAMA_URL = "http://localhost:11434/api/generate"


@router.post("/email/")
def generate_email(email_content: EmailContentInput):
    # prompt = f"Generate an {tone} email as a response from the cutomer support team to the customer for the following email:\n\n{email_content}\n\n" \
    #         "Ensure the response is polite, clear, and professional."
    prompt = f"Write a {email_content.tone} email response:\n\n{email_content.content}"
    payload = {
        "model": "deepseek-r1",
        "prompt": prompt,
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No response available.")


#     test_topic = "The Future of AI"
#     test_keywords = "AI, automation, deep learning"
@router.post("/content-writer/")
def content_writer(content: ContentWriterInput) -> Any:
    # prompt = f"Write an engaging social media post for {platform} about '{topic}'."
    # prompt = f"Write a blog post about '{topic}' in a {tone} tone.\n\n" \
    #         f"Include the following keywords: {keywords}.\n\n" \
    #         f"Ensure the content is well-structured with an introduction, main sections, and a conclusion."

    # prompt = f"Write a blog post about '{topic}' in {language} using a {tone} tone."
    prompt = f"Write a {content.tone} blog post about '{content.topic}' including {content.keywords}."

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No content available.")


@router.post("/resume/")
def generate_resume(data: dict):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Generate resume:\n\n{data}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No resume available.")


def generate_resume(name, job_role, experience, skills, education, summary):
    """
    Uses DeepSeek AI to generate a structured professional resume.
    """
    prompt = (
        f"Generate a professional resume based on the following details:\n\n"
        f"Name: {name}\nJob Role: {job_role}\nExperience: {experience} years\n"
        f"Skills: {skills}\nEducation: {education}\nSummary: {summary}\n\n"
        f"Ensure the resume is ATS-friendly, well-formatted, and professional."
    )

    # prompt = f"Generate a resume in {language}:\n\n{name}, {job_role}, {experience} years, {skills}, {education}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No resume generated.")
    else:
        return f"Error: {response.text}"


def generate_pdf_resume(resume_text, filename="resume.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in resume_text.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(filename)
    return filename


# # Test Resume Generator
# if __name__ == "__main__":
#     test_resume = generate_resume("John Doe", "Software Engineer", "3",
#                                   "Python, AI, Web Development", "B.Sc. CS", "Experienced in AI and cloud computing.")
#     print("### AI-Generated Resume ###")
#     print(test_resume)


@router.post("/meeting_minutes/")
def generate_minutes(transcript: str):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Summarize meeting:\n\n{transcript}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No summary available.")


def generate_meeting_minutes(transcript):
    """
    Uses DeepSeek AI to generate a structured meeting summary.
    """
    prompt = (
        f"Summarize the following meeting transcript into structured meeting minutes:\n\n{transcript}\n\n"
        "Extract key discussions, decisions made, and action items."
    )

    # prompt = f"Summarize this meeting transcript in {language}:\n\n{transcript}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No summary generated.")
    else:
        return f"Error: {response.text}"


def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)


# # Test Meeting Minutes Generator
# if __name__ == "__main__":
#     test_transcript = "John: Q4 sales increased by 15%. Sarah: We need to increase the marketing budget. Decision: Approve higher budget."
#     print("### AI-Generated Meeting Minutes ###")
#     print(generate_meeting_minutes(test_transcript))


@router.post("/extract_text/")
async def extract_text(file: UploadFile = File(...)):
    text = ""
    with fitz.open(file) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"

    return {"extracted_text": text if text.strip() else "No text found in the PDF."}


def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file using PyMuPDF.
    """
    text = ""
    with fitz.open(pdf_file) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"

    return text if text.strip() else "No text found in the PDF."


def exetract_text_with_ocr(pdf_file):
    images = convert_from_path(pdf_file)
    extracted_text = "\n".join(pytesseract.image_to_string(img) for img in images)
    return extracted_text if extracted_text.strip() else "no text found in scanned PDFs"


def summarize_text(text):
    prompt = f"Summarize the following document text:\n\n{text}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No summary available.")


# pdf_path = "sample.pdf"  # Provide a sample PDF file
# print("### Summarized Extracted Text ###")
# # print(extract_text_from_pdf(pdf_path))
# print(summarize_text(extract_text_from_pdf(pdf_path)))
