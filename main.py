from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import requests

import pro


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


@app.get("/")
def home():
    return {"message": "Dumb Question Answers is alive!"}


@app.post("/ask")
def ask_question(data: Question):

    question = data.question.strip()

    question_type = pro.classify_question(question)


    # ---------------- YES / NO ----------------

    if question_type == "yes_no":

        decision = random.choice(["YES", "NO"])

        prompt = f"""
The user asked:

{question}

The decision has already been made: {decision}

Give a short funny, silly, natural reason for this decision.

It should feel like a funny little sign that somehow makes sense.

Do NOT change the decision.
Do NOT repeat the decision.

Maximum 2 short lines.
"""


        ollama_data = {
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }


        response = requests.post(
            "http://localhost:11434/api/generate",
            json=ollama_data
        )


        result = response.json()


        return {
            "type": "yes_no",
            "decision": decision,
            "answer": result["response"].strip()
        }


    # ---------------- OPTIONS ----------------

    elif question_type == "options":

        options = question.split(",")

        options = [
            option.strip()
            for option in options
            if option.strip()
        ]


        winner = random.choice(options)


        prompt = f"""
The chosen option is:

{winner}

Give ONE very short, silly, funny comment about why this option won.

It MUST be exactly one short line.
Do not choose another option.
Do not mention that the choice was random.
"""


        ollama_data = {
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }


        response = requests.post(
            "http://localhost:11434/api/generate",
            json=ollama_data
        )


        result = response.json()
        comment = " ".join(result["response"].strip().split())


        return {
            "type": "options",
            "options": options,
            "winner": winner,
            "answer": comment
        }


    # ---------------- NORMAL ----------------

    else:

        prompt = f"""
Answer this question in a funny, silly, but somehow reasonable way:

{question}

Make it feel like a funny little sign from the universe.

Maximum 2 short lines.
"""

        ollama_data = {
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }


        response = requests.post(
            "http://localhost:11434/api/generate",
            json=ollama_data
        )


        result = response.json()


        return {
            "type": "normal",
            "answer": result["response"].strip()
        }