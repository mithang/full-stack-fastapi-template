from typing import Any

from fastapi import APIRouter
import requests
from pydantic import BaseModel

router = APIRouter(tags=["AI for Developers and Coding"], prefix="/deepseek")


class ContentWriterInput(BaseModel):
    tone: str
    topic: str  # "Professional", "Casual", "Persuasive"
    keywords: str


class EmailContentInput(BaseModel):
    tone: str
    content: str = "Formal"  # "Formal", "Casual", "Friendly"


OLLAMA_URL = "http://localhost:11434/api/generate"


# "Python", "JavaScript", "Java", "C++"
@router.post("/complete_code/")
def complete_code(data: dict):
    # prompt = f"Debug and optimize the following {language} code:\n\n{code_snippet}\n\n" \
    #          "Provide a fixed version with explanations."
    # prompt = f"Explain the following {language} code in simple terms:\n\n{code_snippet}"
    # prompt = f"Complete the following {language} code snippet:\n\n{code_snippet}\n\n" \
    #         "Provide a clean, efficient, and correct implementation."
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Complete code:\n\n{data['code_snippet']}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No completion available.")


@router.post("/generate_sql/")
def generate_sql(data: dict):
    prompt = f"Convert this query into SQL:\n\n{data['natural_query']}\n\nAssume database schema: {data.get('schema', 'unknown')}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No SQL query available.")


# test_query = "List all employees in the Sales department."
def generate_sql_query(
    natural_query,
    database_type="MySQL",
    database_schema="employee(name, salary, department)",
):
    """
    Uses DeepSeek AI to convert a natural language query into an SQL statement.
    """
    # prompt = f"Optimize the following SQL query for better performance:\n\n{sql_query}\n\n" \
    # f"Suggest indexing strategies if necessary."

    prompt = f"Convert this natural language query into {database_type}-compatible SQL:\n\nQuery: {natural_query}"

    prompt = (
        f"Convert the following natural language query into an SQL query:\n\n"
        f"Query: '{natural_query}'\n\n"
        f"Assume the following database schema: {database_schema}.\n"
        f"Return only the SQL query, without explanation."
    )

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No SQL query generated.")
    else:
        return f"Error: {response.text}"


# test_code = "def add_numbers(a, b): return a + b\nprint(add_numbers(5))"
def debug_code(code_snippet, language="Python"):
    """
    Uses DeepSeek AI to analyze code and suggest bug fixes.
    """
    prompt = (
        f"Analyze and debug the following {language} code:\n\n{code_snippet}\n\n"
        "Identify issues, suggest fixes, and return the corrected code along with explanations."
    )

    # prompt = f"Optimize the following {language} code for better performance and efficiency:\n\n{code_snippet}\n\n" \
    #          "Suggest improvements and return the optimized code."

    # prompt = f"Explain the following {language} error message and how to fix it:\n\n{error_message}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No debugging suggestions available.")
    else:
        return f"Error: {response.text}"


@router.post("/generate_docs/")
def generate_docs(data: dict):
    payload = {
        "model": "deepseek-r1",
        "prompt": f"Generate documentation:\n\n{data['code_snippet']}",
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No documentation available.")


def generate_readme(project_description):
    prompt = f"Generate a professional README file for the following project:\n\n{project_description}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No README generated.")


def document_api(code_snippet):
    prompt = f"Generate API documentation for the following code:\n\n{code_snippet}"

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No API documentation available.")


def generate_documentation(code_snippet, language="Python"):
    """
    Uses DeepSeek AI to generate documentation for a given code snippet.
    """
    prompt = (
        f"Generate detailed documentation for the following {language} code:\n\n{code_snippet}\n\n"
        "Add appropriate docstrings, comments, and explanations."
    )

    payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No documentation generated.")
    else:
        return f"Error: {response.text}"


#     test_url = "https://jsonplaceholder.typicode.com/posts/1"
#     print("### AI API Test Output ###")
#     print(test_api(test_url, "GET", expected_fields="userId, id, title, body"))
def test_api(api_url, method="GET", headers=None, payload=None, expected_fields=""):
    """
    Tests an API endpoint and validates the response.
    """
    try:
        headers = headers or {}
        payload = payload or {}

        # Send API request
        if method.upper() == "GET":
            response = requests.get(api_url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(api_url, json=payload, headers=headers)
        else:
            return "Unsupported method. Use GET or POST."

        # Extract response details
        response_time = (
            response.elapsed.total_seconds() * 1000
        )  # Convert to milliseconds
        response_data = response.json()

        # AI-Based Validation Prompt
        prompt = (
            f"Analyze the following API response and check if it contains the required fields: {expected_fields}\n\n"
            f"Response:\n{response_data}\n\n"
            f"Provide validation feedback and missing fields, if any."
        )

        ai_payload = {"model": "deepseek-r1", "prompt": prompt, "stream": False}

        ai_response = requests.post(OLLAMA_URL, json=ai_payload)

        if ai_response.status_code == 200:
            validation_feedback = ai_response.json().get(
                "response", "Validation failed."
            )
        else:
            validation_feedback = "AI validation not available."

        # Construct final output
        output = (
            f"✅ API Test Result:\n"
            f"- Status Code: {response.status_code}\n"
            f"- Response Time: {response_time:.2f}ms\n"
            f"- Validation Feedback:\n{validation_feedback}"
        )

        return output

    except Exception as e:
        return f"Error: {str(e)}"
