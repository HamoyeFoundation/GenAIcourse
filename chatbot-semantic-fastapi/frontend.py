import streamlit as st

from dotenv import load_dotenv
from utils import embed, prompt
from utils.chunking_utils import prep_documents_for_vector_storage
from utils.convo import ChatbotGPT

with st.sidebar:
    st.title('PDF BASED LLM-LANGCHAIN CHATBOT')
    st.markdown('''
    ## About APP:

    The app's primary resource is utilised to create::

    - [streamlit](https://streamlit.io/)
    - [Langchain](https://docs.langchain.com/docs/)
    - [OpenAI](https://openai.com/)
                
                ''')
    
def main():
    st.header("Chat with your pdf file")

    #upload a PDF file
    document = st.file_uploader("Upload your PDF", type="pdf")
    to_embed = st.button("Embed this PDF file")

    if (document is not None) and to_embed:
        st.write(document.name)
        print("sending to vector index")
        ids, texts, metadatas = prep_documents_for_vector_storage(document, streamlit=True)
        embedding_engine = embed.get_embedding_engine()
        vector_index = embed.create_vector_index(
            embed.INDEX_NAME, embedding_engine, texts, metadatas)
        
        query = st.text_input("Ask questions related to your pdf file")

        if query:
            print("connecting to vector storage")
            vector_index = embed.connect_to_vector_index(
                embed.INDEX_NAME, embedding_engine
            )
            print("connected to vector storage")

            sources_and_scores = vector_index.similarity_search_with_score(message, k=5)
            sources, scores = zip(*sources_and_scores)

            print("running query against Q&A chain")

            c = ChatbotGPT("gpt-3.5-turbo-1106", prompt=prompt.main, temperature=0, max_tokens=256)
            response = c.question_answer(sources, query)
            st.write(response)

if __name__ == "__main__":
    main()