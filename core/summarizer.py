from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

topic_summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are a helpful assistant. Given the following document text, divide it into topics based on headings or logical sections, and generate a short bullet point summary for each topic:

Document:
{text}

Summarized by topics:
"""
)

def generate_summary(text):
    chain = LLMChain(llm=llm, prompt=topic_summary_prompt)
    return chain.run(text=text)
