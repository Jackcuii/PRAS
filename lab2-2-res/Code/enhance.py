
import requests
import json
import argparse

input_csv_path = "data/example.csv"
output_csv_path = "results/my_example_results.csv"

syspromptag = "You are a strict prosecutor. You are going to sentence a company for they have flaws in their applications.  Figure out if there is any evidence that they behave poorly."

# sysprompt = "You are an investigator tasked with reviewing sections of a Privacy Policy and Data Safety Declaration from an application."

syspromptto = "You are a staff of a company. Here are some parts of an Privacy Policy and Data Safety Declaration of an application of your company. You are trying to verify that the Data Safety Declaration complies with the Privacy Policy below."

empty = ""

import csv
import os

def remove_empty_lines(content):
    lines = content.split("\n")
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned_lines)


def ask_remote_api(system_prompt, data_safety_content, privacy_policy_content, item):
    
    url = "https://api.theb.ai/v1/chat/completions"
# url = "https://api.baizhi.ai/v1/chat/completions"

    #ctnt = system_prompt + '''You are expected to compare and analyze the information between Data Safety and Privacy Policy to clarify 3 issues: which information is incorrect, \\
    #    which information is incomplete and which information is inconsistent. Notes when classifying: Incomplete: Data Safety provides information but \\
    #    is not as complete as the Privacy Policy provides. Incorrect: Data Safety does not provide that information, but the Privacy Policy mentions it.\\
    #    Inconsistency: Data Safety is provided but its description is inconsistent with the Privacy Policy information provided. Note: always gives me \\
    #    the result (0 or 1, 1 is yes, 0 is no) in the form below: {"incorrect": (0 or 1), "incomplete": (0 or 1), "inconsistent": (0 or 1)}. Please in \\
    #    the answer, just give me the json only and in English. Below is information for 2 parts:\nData Safety: ''' + data_safety_content + '''\nPrivacy \\
    #    Policy:\n''' + privacy_policy_content + ''' '''
    
    ctnt = system_prompt + '''You are expected to compare and analyze the information between Data Safety and Privacy Policy to clarify the issue that 
        which information is inconsistent. Notes when classifying: Inconsistency: Data Safety is provided but its description is inconsistent with the 
        Privacy Policy information provided. Note: always gives me the result (0 or 1, 1 is yes, 0 is no) in the form below: {"'''+ item + '''": (0 or 1)}. 
        Please in the answer, just give me the json only and in English. Below is information for 2 parts:\nData Safety: ''' + data_safety_content + '''\nPrivacy 
        Policy:\n''' + privacy_policy_content + ''' '''
        
    #ctnt = "hello"
        
    print("Requesting: "+ctnt)
    
    payload = json.dumps({"model": "gpt-3.5-turbo","messages": [{"role": "user","content": ctnt}],"stream": False})
    headers = {
        'Authorization': 'Bearer sk-SCTZF4w8GFy07tpgmJDPVGhlQi5BSQA4tusj4TtW9oDK47gK',
        'Content-Type': 'application/json'
    }
    #print("Request sent")
    response = requests.request("POST", url, headers=headers, data=payload)
    #print("Get response")
    jsonized = response.json()
    
    try:
        #if(mol=="gpt-4"):
            #print(jsonized)
        ret = jsonized["choices"][0]["message"]["content"]
    #print(mol+": "+jsonized["choices"][0]["delta"]["content"])
    except json.decoder.JSONDecodeError or KeyError:
        print("Error:")
        print(jsonized)
        print("-----------------------------------")
    return ret
    
    

def my_loop_csv(input_csv_path, output_csv_path, sp_list, item_list, res_list):
    with open(input_csv_path, "r", newline="", encoding="utf-8") as csvfile, open(
        output_csv_path, "w", newline="", encoding="utf-8"
    ) as outputfile:

        reader = csv.reader(csvfile)
        writer = csv.writer(outputfile)

        headers = next(reader)
        writer.writerow(headers)

        for index, row in enumerate(reader):
            print(
                "\n_____________ Run times "
                + str(index + 1)
                + " <"
                + row[0]
                + "> "
                + "_____________"
            )
            for i in range(len(sp_list)):
                sp = sp_list[i]
                item = item_list[i]
                res = res_list[i]
                gpt_result = ask_remote_api(sp, row[4], row[5], item)
                row[headers.index(res)] = remove_empty_lines(
                    gpt_result
                )
            writer.writerow(row)
            print("~~~~~~~~~~~~~~ Success ~~~~~~~~~~~~~~\n")
        

            
my_loop_csv(input_csv_path, output_csv_path, [syspromptto,syspromptag, empty], ["inconsistent", "incorrect", "incomplete"], ["result1", "result2", "result3"])


import pandas as pd
import json

df = pd.read_csv('results/my_example_results.csv')

def extract_result_values(result):
    result_dict = json.loads(result.replace("'", "\""))
    return pd.Series([result_dict.get('inconsistent', 0)])

def extract_result_values2(result):
    result_dict = json.loads(result.replace("'", "\""))
    return pd.Series([result_dict.get('incorrect', 0)])

def extract_result_values3(result):
    result_dict = json.loads(result.replace("'", "\""))
    return pd.Series([result_dict.get('incomplete', 0)])

df['inconsistent'] = df['result1'].apply(extract_result_values)
df['incorrect'] = df['result2'].apply(extract_result_values2)
df['incomplete'] = df['result3'].apply(extract_result_values3)

#df = df.drop(columns=['result'])
df.to_csv('results/my_example_results_processed.csv', index=False)
print("CSV file has been successfully created.")


