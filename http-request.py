import requests
import random
import pro

url = "http://localhost:11434/api/generate"

while True:
    question = input("\nEnter Your Dumb Question For Today🙄: ")
    question_type = pro.classify_question(question)

    if question_type == "yes_no":

        decision = random.choice(["YES", "NO"])

        data = {
           "model": "llama3.2:3b",
            "prompt": f"""
            The question is: {question}
            The decision is: {decision}

            tell me what is the decision and Give a short funny, silly, natural reason for this decision.
            """,
            "stream": False
        }


    elif question_type == "options":

        options = question.split(",")
        winner = random.choice(options)

        data = {
           "model": "llama3.2:3b",
           "prompt": f"""
            The option chosen was: {winner}

           tell me what is the winner and Give a short silly comment about this choice.
            """,
            "stream": False
       }


    else:

        data = {
          "model": "llama3.2:3b",
          "prompt": f"""
          Answer this question in a funny and dumb way:

          {question}
          """,
         "stream": False
        } 


    response = requests.post(
     url,
     json = data
    )
    result = response.json()
    reason = result["response"]
    print(response.status_code)
    result = response.json()
    print(result["response"])