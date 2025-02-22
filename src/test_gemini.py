import llm
from dotenv import dotenv_values

if __name__ == '__main__':
    model = llm.get_model("gemini-1.5-flash-latest")
    model.key = dotenv_values(".env")["GEMINI_API_KEY"]

    q1 = "How many chracters there are in Dickens' Our Mutual Friend? Give me only an estimated number without any elaboration."
    print(f"Asking: {q1}\n\n")
    response = model.prompt(q1)
    print(f"Gemini's response: {response.text()}\n\n")

    q2 = "In Dickens' Our Mutual Friend, how old is the character of Georgina Podsnap? Give me only the age as it stated in the novel or its estimation without any elaboration."
    print(f"Asking: {q2}\n\n")
    response = model.prompt(q2)
    print(f"Gemini's response: {response.text()}\n\n")
