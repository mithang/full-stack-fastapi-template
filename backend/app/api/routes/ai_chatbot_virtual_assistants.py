from typing import Any

from fastapi import APIRouter
import requests
from pydantic import BaseModel
import speech_recognition as sr
import pyttsx3

router = APIRouter(tags=["Chatbots and Virtual Assistants"], prefix="/deepseek")


class ContentWriterInput(BaseModel):
    tone: str
    topic: str  # "Professional", "Casual", "Persuasive"
    keywords: str


class EmailContentInput(BaseModel):
    tone: str
    content: str = "Formal"  # "Formal", "Casual", "Friendly"


OLLAMA_URL = "http://localhost:11434/api/generate"


@router.post("/chatbot/")
def chatbot_response(query: str):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Answer customer query:\n\n{query}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No answer available.")


# Sample FAQ Database
FAQ_DB = {
    "order tracking": "You can track your order by logging into your account and navigating to 'My Orders'.",
    "return policy": "We accept returns within 30 days. Visit our Returns page to initiate a return.",
    "customer support contact": "You can reach customer support at support@example.com or call us at +1-800-555-1234.",
    "payment methods": "We accept Visa, MasterCard, PayPal, and Apple Pay for secure transactions.",
    "shipping details": "Orders are processed within 24 hours. Standard shipping takes 3-5 business days.",
}


def chatbot_response(user_query, language="English"):
    """
    Uses DeepSeek AI to answer customer queries by matching them with predefined FAQ responses.
    """
    prompt = (
        f"Find the best match from the FAQ database for this customer query:\n\n'{user_query}'\n\n"
        f"Available FAQs: {list(FAQ_DB.keys())}\n"
        f"Provide a response based on the closest matching FAQ in {language}."
    )

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        # return "I'm sorry, I couldn't find an answer. Please contact support@example.com for further assistance."
        ai_response = response.json().get(
            "response", "I'm sorry, I don't have an answer for that."
        )
        return FAQ_DB.get(
            ai_response.lower(), ai_response
        )  # Return AI response or predefined answer
    else:
        return "Sorry, I couldn't process your request."


#     sample_query = "How can I return a product?"
#     print("### Chatbot Response ###")
#     print(chatbot_response(sample_query))


@router.post("/assistant/")
def ai_assistant(text: str):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"AI assistant response:\n\n{text}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No answer available.")


# Text-to-Speech Engine
engine = pyttsx3.init()


def ai_assistant(text):
    """
    Uses DeepSeek AI to respond to queries.
    """
    prompt = f"Respond to this query as a personal AI assistant:\n\n{text}"

    # prompt = f"Act as a personal AI assistant. If the user asks for weather, fetch data. Otherwise, respond naturally:\n\n{text}"

    # p
    rompt = f"Respond in {language}:\n\n{text}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        ai_response = response.json().get(
            "response", "I'm sorry, I don't have an answer for that."
        )

        # Convert text to speech
        engine.say(ai_response)
        engine.runAndWait()

        return ai_response
    else:
        return "Sorry, I couldn't process your request."


# Voice Command Function
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"User: {command}")
        return command
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Speech recognition service is unavailable."


# # Test AI Assistant
# if __name__ == "__main__":
#     sample_query = "Tell me a fun fact about space."
#     print("### AI Assistant Response ###")
#     print(ai_assistant(sample_query))

# while True:
#     command = listen_command()
#     if "hey ai" in command.lower():
#         response = ai_assistant(command)
#         print(response)


@router.post("/legal/")
def generate_legal(text: str):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Generate a legal document:\n\n{text}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No contract generated.")


# Legal Document Templates
LEGAL_TEMPLATES = {
    "rental agreement": "Generate a rental agreement between {party1} (tenant) and {party2} (landlord) for {duration} months.",
    "employment contract": "Generate an employment contract between {party1} (employee) and {party2} (employer) with a salary of {salary} per year.",
    "business partnership agreement": "Draft a business partnership agreement between {party1} and {party2}, defining responsibilities and profit-sharing terms.",
    "nda": "Generate a non-disclosure agreement (NDA) between {party1} and {party2} to protect confidential business information.",
}


def generate_legal_document(doc_type, party1, party2, duration="", salary=""):
    """
    Uses DeepSeek AI to generate legal contracts.
    """
    if doc_type not in LEGAL_TEMPLATES:
        return "Invalid document type. Please choose from rental agreement, employment contract, business partnership agreement, or NDA."

    prompt = LEGAL_TEMPLATES[doc_type].format(
        party1=party1, party2=party2, duration=duration, salary=salary
    )

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No document generated.")
    else:
        return f"Error: {response.text}"


# # Test Legal Assistant
# if __name__ == "__main__":
#     print("### AI-Generated Contract ###")
#     print(generate_legal_document("rental agreement", "John Doe", "Jane Smith", duration="12"))


@router.post("/medical/")
def analyze_symptoms(symptoms: str):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Medical symptom analysis:\n\n{symptoms}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No information available.")


def analyze_symptoms(symptoms):
    """
    Uses DeepSeek AI to analyze symptoms and provide possible conditions.
    """
    prompt = (
        f"Analyze the following symptoms and suggest possible health conditions:\n\nSymptoms: {symptoms}\n\n"
        "Provide a short list of possible causes and general advice (no treatment recommendations)."
    )

    # prompt = f"Analyze the following symptoms and classify them as mild, moderate, or severe:\n\nSymptoms: {symptoms}"
    # prompt = f"Analyze symptoms in {language} and provide a response:\n\nSymptoms: {symptoms}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No information available.")
    else:
        return f"Error: {response.text}"


# if __name__ == "__main__":
#     test_symptoms = "Fever, cough, body aches"
#     print("### AI Medical Analysis ###")
#     print(analyze_symptoms(test_symptoms))


@router.post("/recommend/")
def recommend_products(query: str):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Recommend products:\n\n{query}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No recommendations available.")


# Sample Product Dataset
PRODUCT_DB = {
    "laptop": [
        "Apple MacBook Air M2 – Lightweight, powerful, and great battery life.",
        "Dell XPS 13 – High performance with a sleek design.",
        "Lenovo ThinkPad X1 Carbon – Ideal for business professionals.",
    ],
    "smartphone": [
        "iPhone 14 – Great camera and iOS experience.",
        "Samsung Galaxy S23 – High-performance Android flagship.",
        "Google Pixel 7 – Best AI-powered camera features.",
    ],
    "headphones": [
        "Sony WH-1000XM4 – Industry-leading noise cancellation.",
        "Bose QuietComfort 45 – Superior comfort and sound quality.",
        "Anker Soundcore Life Q30 – Best budget ANC headphones.",
    ],
}


def recommend_products(query):
    """
    Uses DeepSeek AI to analyze user intent and suggest relevant products.
    """
    prompt = (
        f"Analyze the following user query and recommend the best matching products:\n\nQuery: '{query}'\n\n"
        f"Available product categories: {list(PRODUCT_DB.keys())}\n"
        f"Provide a list of top recommendations."
    )

    # prompt = f"Find the best {category} within ${max_price}. Recommend top products."

    # prompt = f"Recommend products in {language} based on this query: {query}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        ai_response = response.json().get(
            "response", "I'm sorry, I don't have recommendations for that."
        )

        # Find matching category in database
        for category in PRODUCT_DB:
            if category in query.lower():
                return "\n".join(PRODUCT_DB[category])

        return ai_response
    else:
        return f"Error: {response.text}"


# # Test Product Recommender
# if __name__ == "__main__":
#     test_query = "Recommend a good budget laptop."
#     print("### AI Product Recommendations ###")
#     print(recommend_products(test_query))
