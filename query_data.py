from langchain_chroma import Chroma
import argparse
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = '''
Answer the question only based on the following context:

{context}

---

Answer the question based on the context and format it properly by removing the additional * : {question}

'''
def main():

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="Query text")
    args = parser.parse_args()
    query_text = args.query_text

    #Preparing DB
    gemini_embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=gemini_embedding)

    #Searching DB
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < .6:
        print("Unable to find the information")
        return
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, score in results])
    prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context = context_text, question = query_text)
    llm_model = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
    response = llm_model.invoke(prompt)

    if isinstance(response.content, list):
        print(response.content[0]["text"])
    else:
        print(response.content)
if __name__=="__main__":
    main()