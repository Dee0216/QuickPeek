from langchain_ollama import OllamaLLM
from PyPDF2 import PdfReader
from langchain.prompts import PromptTemplate
from prompts import pdf_analyser_prompt

def extract_text_from_pdf(pdf_path):
	text = ""
	try:
		reader = PdfReader(pdf_path)
		for page in reader.pages:
			text += page.extract_text() + "\n"
	except Exception as e:
		print(f"Error reading PDF: {e}")
	return text.strip()

def summarize_pdf(text):
	llm = OllamaLLM(model="mistral")
	prompt = PromptTemplate(
		input_variables=["content"],
		template=pdf_analyser_prompt
	)
	summary = prompt | llm
	final_summary = summary.invoke({"content": text})
	return final_summary