from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY

llm = ChatOpenAI(model_name="gpt-4o", temperature=0.3,api_key=OPENAI_API_KEY)

doubt_prompt = PromptTemplate(
    input_variables=["query", "context"],
    template="""
Based on the following context from the uploaded document, answer the user's question expressively:

Context:
{context}

Question: {query}

Answer:
"""
)

def ask_ai(query, context):
    chain = LLMChain(llm=llm, prompt=doubt_prompt)
    return chain.run(query=query, context=context)
