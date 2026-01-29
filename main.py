from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# CORS (Flutter Web ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    target_language: str

@app.post("/detect-convert")
def detect_and_convert(req: CodeRequest):

    prompt = f"""
You are a programming language expert.

Tasks:
1. Detect the programming language of the given code.
2. Convert it into {req.target_language}.
3. Keep the logic same.
4. Return ONLY the converted code.
5. No explanation.

Code:
{req.code}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return {
        "converted_code": response.output_text
    }
