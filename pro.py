import random


def classify_question(user_input):
    yes_no_words = [
        "is", "are", "am", "do", "does", "did",
        "can", "could", "should", "would", "will",
        "have", "has"
    ]

    words = user_input.lower().split()
    first_word = words[0]

    if "," in user_input:
        return "options"

    elif first_word in yes_no_words:
        return "yes_no"

    else:
        return "normal"