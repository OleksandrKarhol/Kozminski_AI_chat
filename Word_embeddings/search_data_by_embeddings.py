import pandas as pd
import numpy as np
from ast import literal_eval
from openai.embeddings_utils import get_embedding, cosine_similarity
import openai

openai.api_key = 'YOUR_API_KEY'
datafile_path = "Kozminski_AI_chat/Word embeddings/data/subjects_embeddings_grouped_unique.csv"

df = pd.read_csv(datafile_path)
df["embedding"] = df.embedding.apply(literal_eval).apply(np.array)


# search through the reviews for a specific product
def search_reviews(df, prompt, n=3, pprint=True):
    product_embedding = get_embedding(
        prompt,
        engine="text-embedding-ada-002"
    )
    df["similarity"] = df.embedding.apply(lambda x: cosine_similarity(x, product_embedding))

    results = (
        df.sort_values("similarity", ascending=False)
        .head(n)
        .Category
    )
    if pprint:
        for r in results:
            print(r[:200])
            print()
    return results

results = search_reviews(df, "Can you give me an email of the admission office?", n=3)