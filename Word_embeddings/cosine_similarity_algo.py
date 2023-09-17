import math 
import pandas as pd
import numpy as np 
import ast
from datetime import datetime
from ast import literal_eval
from openai.embeddings_utils import get_embedding, cosine_similarity
import openai
from clean_query import preprocess_text
#from test import test_model

openai.api_key = 'YOUR_API_KEY'

def calc_magnitude ( vector : list ) -> float:
    magnitude = sum( [ a**2 for a in vector ] ) ** 0.5
    return magnitude

def calc_dot_product( vectors : list ) -> float:
    # calculate dimentions
    dims_len = list( set( [ len(v) for v in vectors ] ) )

    dims = [ 1 for i in range(dims_len[0]) ]
    for v in vectors: 
        for i in range(len(dims)):
            dims[i] *= v[i]
    return sum(dims)

def calc_cos ( vector, query ) -> float:
    # make the length of both vectors equal
    vectors = populate_with_zeros( vector, query )
    # calc magnitude 
    vectorMagnitudes = ( list( map( calc_magnitude, vectors ) ) )
    finalMagnitude = math.prod(vectorMagnitudes)
    # calc dot products
    dotProduct = calc_dot_product(vectors)
    #calc cosine 
    cos = dotProduct / finalMagnitude
    return cos

def populate_with_zeros( vector, query ):
    if len(vector) > len(query): 
        query += [0] * ( len(vector) - len(query) )
    elif len(vector) < len(query): 
        vector += [0] * ( len(query) - len(vector) )
    return [ vector, query ]

def find_matching_case(query : str):
    
    print('process started', datetime.now())
    
    # embeddings dataset
    df = pd.read_csv( 'Kozminski_AI_chat/Word_embeddings/data/subjects_embedding.csv' ) 
    query = cleanQuery(query)
    query_embedding = get_embedding(
        query,
        engine="text-embedding-ada-002"
    )

    print('Query embeddings are ready', datetime.now())

    df["embedding"] = df.embedding.apply(literal_eval).apply(np.array)
    embeddings = list(df.embedding)

    row_cos = [ calc_cos( row, query_embedding ) for row in embeddings]
    df['cosine_scores'] = row_cos
    
    results = (
        df.sort_values( "cosine_scores", ascending=False )
        .head(1)
        .Category
    ).to_string(index=False)

    print(results)
    return str(results)

def cleanQuery(query):
    cleaned_query = preprocess_text(query)
    #return query
    return cleaned_query

if __name__ == "__main__":
    find_matching_case('What is the application deadline')
    # test_model(find_matching_case, 8)
    #query = " I'm studying in Kozminski on the second year of my bachelor's degree, when and where will the next internship fair take place? "
    #print( find_matching_case( query ) )
    #print( "process finished", datetime.now() )