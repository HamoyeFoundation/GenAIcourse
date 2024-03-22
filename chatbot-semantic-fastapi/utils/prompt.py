from langchain.prompts import PromptTemplate

template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {sources} 
Answer:"""

main = PromptTemplate(template=template, input_variables=["question", "sources"])

per_source = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)
