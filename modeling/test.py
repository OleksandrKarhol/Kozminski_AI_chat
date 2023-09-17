import pandas as pd
import openpyxl
import os
from tqdm import tqdm 

REULTS_FILE_PATH = 'Kozminski_AI_chat/testing_models/results_reduced_data.xlsx'

def import_questions():
    global questions_df
    questions_df = pd.read_excel('Kozminski_AI_chat/testing_models/test_set.xlsx')
    print(questions_df.columns)
    return questions_df

def create_results_df():# create a file with results
    if os.path.exists( REULTS_FILE_PATH ):
        pass
    else:
        results_df = pd.DataFrame( [], columns = [ 'Question', 'Category', 'NN_BOW', 'NN_embeddings' ] )
        results_df[ 'Question' ] = questions_df[ 'Question' ]
        results_df[ 'Category' ] = questions_df[ 'Category' ]
        results_df.to_excel( REULTS_FILE_PATH , index = None)

# iterate through questions 
def test_model( model, model_name : int ):
    
    questions_df = import_questions()
    create_results_df()

    for index, row in tqdm( questions_df.iterrows() ):
        # get answer
        question = row['Question'] 
        print(question)
        answer = model( question )
        print(answer, type(str(answer)))

        # Update the Excel file
        workbook = openpyxl.load_workbook( REULTS_FILE_PATH )
        sheet = workbook[ 'Sheet1' ]
        sheet.cell( row=index+2, column = model_name, value = answer)
        workbook.save( REULTS_FILE_PATH )