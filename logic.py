import os
import sys
from modules import *

load_dotenv()
api_key = os.getenv("API_KEY")

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

chain = None

def start_chat():
    global chain
    try:
        if PERSIST and os.path.exists("persist"):
            print("Reusing index...\n")
            vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
            index = VectorstoreIndexCreator(vectorstore=vectorstore).from_loaders([])
        else:
            loader = TextLoader("data/data.txt")
            #loader = DirectoryLoader("data/")
            index = VectorstoreIndexCreator(vectorstore_cls=Chroma,
                embedding=OpenAIEmbeddings(),
                vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model="gpt-3.5-turbo"),
            retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
        )
    except Exception as e:
        print(f"An error occurred during setup: {str(e)}")
        sys.exit(1)

def process_chat(query, chat_history):
    global chain
    if chain is None:
        raise Exception("Chat not started. Call start_chat() first.")
    result = chain.invoke({"question": question, "chat_history": chat_history})
    chat_history.append((question, result['answer']))
    return result['answer'], chat_history