from typing import Any

from fastapi import APIRouter
import requests
from pydantic import BaseModel

router = APIRouter(tags=["AI Text Processing and NLP"], prefix="/deepseek")


OLLAMA_URL = "http://localhost:11434/api/generate"


class SummarizeRequest(BaseModel):
    text: str


class GenerateRequest(BaseModel):
    prompt: str
    word_limit: int = 100


class CorrectionRequest(BaseModel):
    text: str


@router.post("/summarize/")
def summarize_text(request: SummarizeRequest):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Summarize:\n\n{request.text}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No summary generated.")


def summarize_text(text):
    """
    Uses DeepSeek AI to summarize a given text.
    """

    payload = {
        "model": "deepseek-r1",
        "prompt": f"Summarize the following text in **3 bullet points**:\n\n{text}",
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No summary generated.")
    else:
        return f"Error: {response.text}"


# if __name__ == "__main__":
#     sample_text = """
#     Artificial Intelligence is transforming industries across the world. AI models like DeepSeek-R1 enable businesses to automate tasks,
#     analyze large datasets, and enhance productivity. With advancements in AI, applications range from virtual assistants to predictive analytics
#     and personalized recommendations.
#     """
#     print("### Summary ###")
#     print(summarize_text(sample_text))


@router.post("/generate/")
def generate_text(request: GenerateRequest):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Generate {request.word_limit} words:\n\n{request.prompt}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No content generated.")


def generate_text(prompt, word_limit=100, language="English"):
    """
    Uses DeepSeek AI to generate text based on a given prompt.
    """
    full_prompt = f"Write a {language}-language text to Generate a response within {word_limit} words:\n\n{prompt}"

    payload = {"model": "deepseek-r1", "prompt": full_prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No content generated.")
    else:
        return f"Error: {response.text}"


# # Test AI Generation
# if __name__ == "__main__":
#     prompt = "Write an introduction for an article about the future of AI."
#     print("### AI-Generated Content ###")
#     print(generate_text(prompt))


@router.post("/correct/")
def correct_grammar(request: CorrectionRequest):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Correct grammar:\n\n{request.text}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No correction generated.")


def correct_grammar(text):
    """
    Uses DeepSeek AI to correct grammar and spelling errors in the given text.
    """
    prompt = f"Correct any spelling and grammar mistakes in the following text and provide explanations:\n\n{text}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No correction generated.")
    else:
        return f"Error: {response.text}"


# # Test Grammar Correction
# if __name__ == "__main__":
#     sample_text = "He dont like to eat apple because they taste sour."
#     print("### Corrected Text ###")
#     print(correct_grammar(sample_text))


@router.post("/extract_entities/")
def extract_named_entities(text: str):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Extract entities:\n\n{text}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No entities detected.")


def extract_named_entities(text):
    """
    Uses DeepSeek AI to identify named entities (people, organizations, locations, dates).
    """
    prompt = f"Extract all named entities (persons, organizations, locations, dates) from the following text:\n\n{text}"
    # prompt = f"Extract persons, organizations, locations, dates, and job titles from this French-language text:\n\n{text}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No entities detected.")
    else:
        return f"Error: {response.text}"


# # Test Named Entity Recognition
# if __name__ == "__main__":
#     sample_text = "Google was founded by Larry Page and Sergey Brin in September 1998 at Stanford University."
#     print("### Extracted Entities ###")
#     print(extract_named_entities(sample_text))


@router.post("/analyze_sentiment/")
def analyze_sentiment(text: str):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Classify sentiment:\n\n{text}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No sentiment detected.")


def analyze_sentiment(text, language="Engligh"):
    """
    Uses DeepSeek AI to classify sentiment as positive, negative, or neutral.
    """
    # prompt = f"Classify the sentiment of the following text as Positive, Negative, or Neutral:\n\n{text}"
    # prompt = f"Analyze the sentiment of this text. Provide a sentiment score from -1 (very negative) to +1 (very positive):\n\n{text}"
    # prompt = f"Classify the sentiment of this text (in {language}) as Positive, Negative, or Neutral:\n\n{text}"
    prompt = f"Identify sentiment in the following text and highlight words that contribute to it:\n\n{text}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No sentiment detected.")
    else:
        return f"Error: {response.text}"


# # Test Sentiment Analysis
# if __name__ == "__main__":
#     # sample_text = "The movie was absolutely fantastic! I enjoyed every minute of it."
#     sample_text = "The service was terrible. I waited an hour, and my order was wrong."
#     print("### Sentiment Analysis Result ###")
#     print(analyze_sentiment(sample_text))
