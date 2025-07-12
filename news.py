from newspaper import Article
import requests
from bs4 import BeautifulSoup
from langchain_ollama  import OllamaLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from prompts import news_analyser_prompt

def extract_article_content(url):
    headers = {
        'User-Agent':'Mozilla/5.0'
    }
    response = requests.get(url,headers=headers, timeout=10)
    soup=BeautifulSoup(response.text,'html.parser')
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else "No title found"
    paragraph = soup.find_all('p')
    content = " ".join(p.get_text() for p in paragraph)
    return title.strip(), content.strip()

def summarize_article(article_text):
    llm = OllamaLLM(model="mistral")
    prompt = PromptTemplate(
        input_variables=["content"],
        template=news_analyser_prompt
    )
    response =prompt|llm
    final_response = response.invoke({"content": article_text})
    return final_response
