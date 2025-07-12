from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from prompts import summary_breif

def elaborate_summary(summary_text):
    llm = OllamaLLM(model="mistral")
    prompt = PromptTemplate(
        input_variables=["content"],
        template=summary_breif
    )
    response = prompt | llm
    final = response.invoke({"content": summary_text})
    return final
