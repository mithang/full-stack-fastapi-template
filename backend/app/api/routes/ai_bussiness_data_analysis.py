from typing import Any

from fastapi import APIRouter
import requests
from pydantic import BaseModel

router = APIRouter(tags=["AI for Business and Data Analysis"], prefix="/deepseek")


class ContentWriterInput(BaseModel):
    tone: str
    topic: str  # "Professional", "Casual", "Persuasive"
    keywords: str


class EmailContentInput(BaseModel):
    tone: str
    content: str = "Formal"  # "Formal", "Casual", "Friendly"


OLLAMA_URL = "http://localhost:11434/api/generate"


#     test_feedback = "I love the laptop's performance, but the keyboard feels cheap."
#     print("### AI Feedback Analysis ###")
#     print(analyze_feedback(test_feedback))
@router.post("/analyze_feedback/")
def analyze_feedback(data: dict):
    prompt = f"Analyze customer feedback:\n\n{data['feedback']}\n\nProvide sentiment and insights."

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No analysis available.")


def analyze_feedback(feedback_text):
    """
    Uses DeepSeek AI to analyze customer feedback and extract insights.
    """
    prompt = (
        f"Analyze the following customer feedback:\n\n{feedback_text}\n\n"
        "Provide sentiment analysis (positive, neutral, negative), key themes, and actionable insights."
    )

    # prompt = f"Analyze the customer feedback and classify it into categories like Product, Service, Price, Delivery:\n\n{feedback_text}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No insights generated.")
    else:
        return f"Error: {response.text}"


def fetch_latest_news(category="technology", country="us"):
    """
    Fetches the latest news articles from NewsAPI based on category and country.
    """
    url = f"https://newsapi.org/v2/top-headlines?category={category}&country={country}&apiKey={NEWS_API_KEY}"

    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        if not articles:
            return "No news articles found."

        # Extract title and content from the first article
        news_title = articles[0]["title"]
        news_content = articles[0]["description"] or articles[0]["content"]

        return news_title, news_content
    else:
        return "Error fetching news."


def summarize_news(category="technology", country="us"):
    """
    Fetches and summarizes the latest news article.
    """
    news_title, news_content = fetch_latest_news(category, country)

    if news_content == "No news articles found.":
        return "No news available for this category."

    # Generate summary using DeepSeek AI
    prompt = (
        f"Summarize the following news article:\n\nTitle: {news_title}\n\nContent: {news_content}\n\n"
        "Provide a short and informative summary."
    )

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        summary = response.json().get("response", "No summary generated.")
    else:
        summary = "Error summarizing news."

    return f"📰 **{news_title}**\n📅 **Category:** {category.capitalize()}\n🔹 **Summary:** {summary}"


# def search_news(keyword):
#     url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={NEWS_API_KEY}"


# def fetch_news_from_source(source="nytimes", category="technology"):
#     url = f"https://api.nytimes.com/svc/topstories/v2/{category}.json?api-key=your_nytimes_api_key"
#     print("### AI News Summary ###")
#     print(summarize_news("technology"))


@router.post("/analyze_financials/")
def analyze_financials(data: dict):
    prompt = f"Analyze financial report:\n\n{data['report']}\n\nProvide insights and detect trends."

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No analysis available.")


# def analyze_uploaded_financial_report(file):
#     df = pd.read_csv(file.name) if file.name.endswith(".csv") else pd.read_excel(file.name)
#     financial_data = df.to_string()
#     return analyze_financial_report(financial_data)


#     test_financial_data = "Company: ABC Inc, Revenue: $75M, Net Profit: $12M, Expenses: $50M, Debt: $10M"
#     print("### AI Financial Analysis ###")
#     print(analyze_financial_report(test_financial_data))
def analyze_financial_report(financial_data):
    """
    Uses DeepSeek AI to analyze a financial statement and extract insights.
    """
    prompt = (
        f"Analyze the following financial report:\n\n{financial_data}\n\n"
        "Extract key financial metrics, detect trends, and provide a structured summary."
    )

    # prompt = f"Analyze the following financial report for anomalies:\n\n{financial_data}\n\n" \
    #      "Identify unusual revenue changes, unexpected expenses, and financial risks."

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No financial insights generated.")
    else:
        return f"Error: {response.text}"


@router.post("/screen_candidate/")
def screen_candidate(data: dict):
    prompt = f"Analyze resume:\n\n{data['resume']}\n\nCompare with job description:\n\n{data['job_description']}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No analysis available.")


def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a resume PDF file.
    """
    text = ""
    with fitz.open(pdf_file.name) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text if text.strip() else "No text found in the PDF."


# def screen_multiple_candidates(resume_list, job_description):
#     results = [screen_candidate(resume, job_description) for resume in resume_list]
#     return "\n\n".join(results)


def screen_candidate(resume_text, job_description):
    """
    Uses DeepSeek AI to analyze a resume and compare it with a job description.
    """

    prompt = (
        f"Analyze the following resume and compare it with the job description.\n\n"
        f"Resume:\n{resume_text}\n\n"
        f"Job Description:\n{job_description}\n\n"
        "Provide a suitability score (0-100%) based on skills and experience. Highlight matches and missing criteria."
    )

    # prompt += " Suggest ways for the candidate to improve their qualifications for this role."

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No analysis generated.")
    else:
        return f"Error: {response.text}"


#     test_resume = "Name: John Doe, Experience: 1 years in Web Development, Skills: Java, Education: B.Sc. in Mechanical Engineering"
#     test_job_description = "Role: Backend Engineer, Required Skills: Python, Flask, SQL, API Development, Experience: 3+ years"

#     print("### AI Screening Report ###")
#     print(screen_candidate(test_resume, test_job_description))


# # Test AI Research Paper Summarizer
# if __name__ == "__main__":
#     test_paper = "This study examines how AI impacts climate change predictions using deep learning models..."
#     print("### AI-Generated Research Paper Summary ###")
#     print(summarize_research_paper(test_paper))
@router.post("/summarize_paper/")
def summarize_paper(data: dict):
    prompt = (
        f"Summarize research paper:\n\n{data['paper_text']}\n\nExtract key insights."
    )

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No summary available.")


def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a research paper PDF.
    """
    text = ""
    with fitz.open(pdf_file.name) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text if text.strip() else "No text found in the PDF."


# def extract_relevant_sections(paper_text):
#     prompt = f"Extract key sections (abstract, methodology, results, conclusion) from the following research paper:\n\n{paper_text}"


def summarize_research_paper(paper_text):
    """
    Uses DeepSeek AI to summarize an academic research paper.
    """
    prompt = (
        f"Summarize the following academic research paper:\n\n{paper_text}\n\n"
        "Extract key sections (abstract, introduction, methodology, results, conclusion) and generate a structured summary."
    )

    # prompt += " Also, classify the research paper into a relevant category (e.g., AI, Medicine, Physics)."

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No summary generated.")
    else:
        return f"Error: {response.text}"
