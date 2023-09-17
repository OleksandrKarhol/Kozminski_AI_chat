# imports
import pandas as pd
import openai 
from openai.embeddings_utils import get_embedding

openai.api_key = 'YOUR_API_KEY'

# embedding model parameters
embedding_model = "text-embedding-ada-002" # try another models
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

# load & inspect dataset
input_datapath = 'Kozminski_AI_chat/Word_embeddings/data_reduced/subjects_data_cleaned.csv'  # to save space, we provide a pre-filtered dataset
df = pd.read_csv(input_datapath, index_col=0)
#df = pd.read_excel(input_datapath)

# This may take a few minutes
df["embedding"] = df.Question.apply(lambda x: get_embedding(x, engine=embedding_model))
df.to_csv("data/subjects_embeddings.csv", index=None)