
import pandas as pd
import json

df = pd.read_csv('results/my_example_results.csv')

def extract_result_values(result):
    result_dict = json.loads(result.replace("'", "\""))
    return pd.Series([result_dict.get('inconsistent', 0)])

def extract_result_values2(result):
    result_dict = json.loads(result.replace("'", "\""))
    return pd.Series([result_dict.get('incorrect', 0)])

df['inconsistent'] = df['result1'].apply(extract_result_values)
df['incorrect'] = df['result2'].apply(extract_result_values2)
df['incomplete'] = df['result3'].apply(extract_result_values3)

#df = df.drop(columns=['result'])
df.to_csv('results/my_example_results_processed.csv', index=False)
print("CSV file has been successfully created.")
