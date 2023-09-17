import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

def make_matrix(y_predicted_column_name):# Load your Excel file into a Pandas DataFrame
    file_path = 'results.xlsx'
    data = pd.read_excel(file_path)

    # replace recently changed categories
    #data[f'{y_predicted_column_name}'] = data[f'{y_predicted_column_name}'].replace('Study and Internship abroad', 'Internship')

    # Extract actual and predicted labels
    actual_labels = data['Category']
    predicted_labels = data[y_predicted_column_name]
    
    y_labels = ['About University', 'Admissions and Application Process', 'Campus', 'Contacts', 'Double Degree programs', 
          'Educational resources', 'Insurance', 'Internship', 'Languege Courses', 'Open Days', 'Programmes and Degrees', 
         'Scholarship', 'Scientific Research', 'Student Housing', 'Study and Internship abroad']
    y_labels_predicted = list(set(predicted_labels))
    y_lables_actual = list(set(actual_labels))


    # Create a confusion matrix
    conf_matrix = confusion_matrix(actual_labels, predicted_labels)

    # Create a heatmap for the confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
                xticklabels = y_labels,
                yticklabels = y_labels)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()

    # Save the heatmap as a PNG image
    plt.savefig(f"confusion_matrix_{y_predicted_column_name}.png")
    print(f'File "confusion_matrix_{y_predicted_column_name}.png" saved')
    plt.show()



def calculate_accuracy(y_predicted_column_name):
    file_path = 'results.xlsx'
    data = pd.read_excel(file_path)

    # replace recently changed categories
    #data[f'{y_predicted_column_name}'] = data[f'{y_predicted_column_name}'].replace('Study and Internship abroad', 'Internship')

    correctness_list = []
    for index, row in data.iterrows():
        if row[f'{y_predicted_column_name}'] == row['Category']:
            correctness_list.append(1)
        else: correctness_list.append(0)

    average_accuracy = sum(correctness_list) / len(correctness_list)
    print(f'average accuracy of {y_predicted_column_name} is: ', average_accuracy)



def calculate_validated_accuracy(column_names : list):
    file_path = 'results.xlsx'
    data = pd.read_excel(file_path)

    # replace recently changed categories
    #data[f'{column_names[0]}'] = data[f'{column_names[0]}'].replace('Study and Internship abroad', 'Internship')
    #data[f'{column_names[1]}'] = data[f'{column_names[1]}'].replace('Study and Internship abroad', 'Internship')

    correctness_list = []
    for index, row in data.iterrows():
        if row[f'{column_names[0]}'] == row['Category'] or row[f'{column_names[1]}'] == row['Category']:
            correctness_list.append(1)
        else: correctness_list.append(0)

    average_accuracy = sum(correctness_list) / len(correctness_list)
    print(f'average validated accuracy of is: ', average_accuracy)


if __name__ == '__main__':
    column_names = ['NN_tokens', 'NN_embeddings']
    for column in column_names: 
        #make_matrix(column)
        calculate_accuracy(column)
    
    calculate_validated_accuracy(column_names)
