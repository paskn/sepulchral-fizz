from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


def main():
    template = """Question: {question}
    Answer: Let's think step by step."""
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="llama3.2:latest")
    chain = prompt | model
    print(chain.invoke({"question": "What is a character in a novel? How scholars define and finde them?"}))


if __name__ == "__main__":
    main()
