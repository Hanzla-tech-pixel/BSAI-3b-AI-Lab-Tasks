# Task 1 — task1_tokens.py
import re
from sklearn.feature_extraction.text import TfidfVectorizer

samples = [
    "AI, search!",
    "I can't log in.",
    "help@example.com",
    "CS4944 version 2.1",
    "",
    "یہ ایک ٹیسٹ مثال ہے"
]

print("=" * 60)
print("TASK 1: TOKENIZATION")
print("=" * 60)

for text in samples:
    whitespace = text.split()
    word_tokens = re.findall(r"\b\w+\b", text, flags=re.UNICODE)

    print("\nOriginal:", repr(text))
    print("Whitespace tokens:", whitespace, len(whitespace))
    print("Word-like tokens:", word_tokens, len(word_tokens))

FAQ = [
    {
        "question": "How do I reset my password?",
        "answer": "Use the recovery link on the login page.",
        "source": "it_help.txt"
    },
    {
        "question": "Where do I submit my assignment?",
        "answer": "Upload it through the learning portal.",
        "source": "assessment.txt"
    },
    {
        "question": "Can illness justify late submission?",
        "answer": "Request an extension with medical evidence before the deadline.",
        "source": "handbook.txt"
    },
    {
        "question": "How can I connect to campus Wi-Fi?",
        "answer": "Select the campus network and sign in with your student account.",
        "source": "it_help.txt"
    },
    {
        "question": "How long can I borrow a library book?",
        "answer": "A library book can be borrowed for fourteen days.",
        "source": "library_rules.txt"
    }
]

questions = [item["question"] + " " + item["answer"] for item in FAQ]

vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(questions)


def chatbot(query):
    if not query.strip():
        return "Please enter a question."

    for item in FAQ:
        if query.strip().casefold() == item["question"].casefold():
            return item["answer"] + " [Source: " + item["source"] + "]"

    query_vector = vectorizer.transform([query])

    if query_vector.nnz == 0:
        return "No matching FAQ found. Contact the help desk."

    scores = (query_vector @ matrix.T).toarray()[0]
    ranked = scores.argsort()[::-1][:3]

    result = ["Possible matching questions:"]

    for index in ranked:
        result.append(
            FAQ[index]["question"] +
            " (Similarity: " + str(round(scores[index], 3)) + ")"
        )

    return "\n".join(result)


print("\nFAQ CHATBOT TEST")

test_questions = [
    "How do I reset my password?",
    "password recovery",
    "",
    "volcano geology"
]

for question in test_questions:
    print("\nUser:", question)
    print("Bot:", chatbot(question))

print("\nTokenization can divide the same text differently.")
print("For example, regex separates 'can't' into 'can' and 't'.")
print("Removing punctuation may also change the meaning of text.")
print("A similarity score is not proof that an answer is correct.")


