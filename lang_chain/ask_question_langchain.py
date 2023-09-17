import os
import sys
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  loader = TextLoader("Kozminski_AI_chat/lang_chain/data/test_set.txt")
  #loader = DirectoryLoader('/Users/apple/Desktop/chat_project/scraping/archive_big')
  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(model='gpt-3.5-turbo'),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []
while True:
  if not query:
    query = """YOUR TASK IS TO CLASSIFY THE USER PTOMPT. WHATEVER THE USER ASKS, DO NOT ANSWER THE 
    QUESTION. INSTEAD, ALWAYS GIVE A LINK TO THE PROGRAM THAT THE USER ASKS ABOUT. NEVER USE ANY OTHER TEXT IN THE ANSWER.
    USE THIS FORMAT FOR EACH ANSWER : "LINK: https://example_link.com". YOUR GOAL IS TO 
    IDENTIFY WHAT THE PROGRAM IS THAT USER IS INTERESTED IN. IF YOU DO NOT KNOW THE ANSWER, THEN RETURN
    "LINK: None". THE USER PROMPT: 
    """ + input("Prompt: ")
  if query in ['quit', 'q', 'exit']:
    sys.exit()
  result = chain({"question": query, "chat_history": chat_history})
  print(result['answer'])

  chat_history.append((query, result['answer']))
  query = None