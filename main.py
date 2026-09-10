from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import random
import requests
import os

from dotenv import load_dotenv

import pro


load_dotenv()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-3.5-flash:generateContent"
)


def ask_gemini(prompt):

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY is not set")

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        GEMINI_URL,
        headers={
            "x-goog-api-key": GEMINI_API_KEY,
            "Content-Type": "application/json"
        },
        json=data
    )

    print("Gemini status:", response.status_code)
    print("Gemini response:", response.text)

    response.raise_for_status()

    result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]


@app.post("/ask")
def ask_question(data: Question):

    try:

        print("ASK ENDPOINT REACHED")
        print("Question:", data.question)

        question = data.question.strip()

        question_type = pro.classify_question(question)

        print("Question type:", question_type)


        # YES / NO

        if question_type == "yes_no":

            decision = random.choice([
                "YES",
                "NO"
            ])

            prompt = f"""
The user asked:

{question}

The decision has already been made:

{decision}

Give a short funny, silly, natural reason for this decision.

It should somehow make sense and feel like a funny little
sign from the universe.

Do NOT change the decision.
Do NOT repeat the decision.

Maximum 2 short lines.
"""

            answer = ask_gemini(prompt)

            answer = " ".join(answer.strip().split())

            return {
                "type": "yes_no",
                "decision": decision,
                "answer": answer
            }


        # OPTIONS

        elif question_type == "options":

            options = [
                option.strip()
                for option in question.split(",")
                if option.strip()
            ]

            winner = random.choice(options)

            prompt = f"""
The chosen option is:

{winner}

Give ONE very short, silly and funny comment
about why this option won.

It MUST be exactly one short line.

Do not choose another option.
Do not mention that the choice was random.
"""

            answer = ask_gemini(prompt)

            answer = " ".join(answer.strip().split())

            return {
                "type": "options",
                "options": options,
                "winner": winner,
                "answer": answer
            }


        # NORMAL QUESTION

        else:

            prompt = f"""
Answer this question in a funny, silly,
but somehow reasonable way:

{question}

Make it feel like a funny little sign from the universe.

Maximum 2 short lines.
"""

            answer = ask_gemini(prompt)

            answer = " ".join(answer.strip().split())

            return {
                "type": "normal",
                "answer": answer
            }


    except Exception as error:

        print("REAL ERROR:", repr(error))

        return {
            "error": str(error)
        }


# Serve the frontend

app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)

