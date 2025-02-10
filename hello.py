from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


# TODO: implement a function that takes a string and counts how many words it has
def count_words(text: str) -> int:
    """Counts the number of words in a string.

    Words are separated by spaces.
    """
    return len(text.split())


def main():
    template = """Question: {question}
    Answer: Let's think step by step."""
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="llama3.2:latest")
    chain = prompt | model
    question = "What is a character in a novel? How scholars define and finde them?"
    print(f"The question has {count_words(question)} words")
    print(chain.invoke({"question": question}))


if __name__ == "__main__":
    main()
