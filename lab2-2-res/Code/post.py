

import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
import matplotlib.pyplot as plt


actual_data = pd.read_csv("data/example_groudtruth.csv")
predict_data = pd.read_csv("results/my_example_results_processed.csv")

actual_data = actual_data[["incorrect", "incomplete", "inconsistent"]]
predict_data = predict_data[["incorrect", "incomplete", "inconsistent"]]


for column in actual_data.columns:
    cm = confusion_matrix(actual_data[column], predict_data[column])

    precision = precision_score(actual_data[column], predict_data[column])
    recall = recall_score(actual_data[column], predict_data[column])
    f1 = f1_score(actual_data[column], predict_data[column])
    accuracy = accuracy_score(actual_data[column], predict_data[column])

    print(f"========== {column}:")
    print(cm)
    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print(f"F1: {f1:.3f}")
    print(f"Accuracy: {accuracy:.3f}")
    print()
    
    
def plot_confusion_matrix(cm, title):
    plt.imshow(cm, interpolation='nearest')
    plt.title(title)
    plt.colorbar()

    classes = ['Right', 'Wrong']
    plt.xticks(range(len(classes)), classes)
    plt.yticks(range(len(classes)), classes)
    
    # show axis
    plt.xlabel('Predicted')
    plt.ylabel('Actual')

    for i in range(len(cm)):
        for j in range(len(cm[0])):
            plt.text(j, i, cm[i, j], ha='center', va='center')

    plt.show()

for column in actual_data.columns:
    cm = confusion_matrix(actual_data[column], predict_data[column])
    plot_confusion_matrix(cm, f"Confusion Matrix for {column}")
