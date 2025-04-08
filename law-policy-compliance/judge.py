__package__ = 'pras'

from llm import ask_model
import json

debate_iter = 6

Investigator0_prefix = "You are an Investigator. Here is a part of an App's User Privacy Policy. Read the Private Policy and figure out whether it is possible to violates the GDPR. Just tell me \"yes\" (may violate) or \"no\" (non-violation). Do not tell me anything else. "
Investigator1_prefix = "You are an Investigator. Here are a piece of an App's User Privacy Policy and a GDPR article. Read the Private Policy and figure out whether it is related to the given GDPR article. Just tell me \"yes\" (related) or \"no\" (non-related). Do not tell me anything else. "
Prosecutor0_prefix = "You are a Prosecutor in the court who is going to sentence a company by violating GDPR. The offcials collected some evidences. You are going to read the given privacy policy piece and the given GDPR item. Then decide whether to sentence the company for breaking the given article. You should answer me with \{ \"decision\" : \"yes\"/\"no\" , \"explanation\": \"...\" \} Do not includes any other words or markdown format."
Lawyer_prefix = "You are a Defense Lawyer in the court who is going to defend a company from being sentenced by violating GDPR. You should try to dispute the prosecutor's statements and be coherent with you own past statements. You should only includes your words in reply. Do not say anything else."
Prosecutor1_prefix = "You are a Prosecutor in the court who is going to sentence a company by violating GDPR. You should try to dispute the lawyer's statements and be inherent with you own past statements (Just be coherent in meaning, do not need to obey the json format given to you last time). You should only includes your words in reply. Do not say anything else."
Judge_prefix = "You are a Judge in the court who is going to decide whether to sentence a company by violating GDPR. You should comprehend the debate between the prosecutor and the lawyer and find out who is right. Then you should decide whether to sentence the company or not. You should answer me with \{ \"decision\" : \"guilty\"/\"innocent\" , \"explanation\": \"...\" \} Do not includes any other words or markdown format."


def compare_result(result, gt):
    """
    Compare the result with the ground truth
    result: list of results from start_court
    gt: list of ground truth
    """
    false_positive = 0
    false_negative = 0
    true_positive = 0
    true_negative = 0
    for i in range(len(result)):
        if result[i] == 1 and gt[i] == 0:
            false_positive += 1
        elif result[i] == 0 and gt[i] == 1:
            false_negative += 1
        elif result[i] == 1 and gt[i] == 1:
            true_positive += 1
        elif result[i] == 0 and gt[i] == 0:
            true_negative += 1
    
    return false_positive, false_negative, true_positive, true_negative

def start_court(policies, items, gt):
    """
    policies: list of privacy policies
    items: list of GDPR items
    gt: list of ground truth
    gt and policies should be the same length
    """
    result = []
    for i in range(len(policies)):
        policy_result = []
        for j in range(len(items)):
            print("--------------------------------------------------")
            print(">>>>>> Line ", i, "/", len(policies), " and ", j, "/", len(items))
            print("Start the judgement: ")
            print("Privacy Policy: ", policies[i])
            print("GDPR Item: ", items[j])
            print("Ground Truth: ", gt[i])
            print("--------------------------------------------------")
            policy_result += [start_judgement(policies[i], items[j])]
        # if none of the items are violated, then the result should be 0
        if all(x == 0 for x in policy_result):
            result += [0]
        else:
            result += [1]
    
    assert len(result) == len(policies)
    assert len(result) == len(gt)
    
    return result
    
    

def start_judgement(policy, item):
    
    policy = "<privacy policy>" + policy + "</privacy policy>"
    item = "<GDPR item>" + item + "</GDPR item>"
    # 1. search evidences
    print("God to I0: ")
    Investigator0_input = Investigator0_prefix + policy
    print(Investigator0_input)
    print("Investigator0: ")
    Investigator0_response = ask_model(Investigator0_input)
    print(Investigator0_response)
    if not ("yes" in Investigator0_response):
        return 0
    print("-----------------------------------------------")
    
    print("God to I1: ")
    Investigator1_input = Investigator1_prefix + policy + item
    print(Investigator1_input)
    print("Investigator1: ")
    Investigator1_response = ask_model(Investigator1_input)
    print(Investigator1_response)
    if not ("yes" in Investigator1_response):
        return 0
    print("-----------------------------------------------")
    
    # 2. identify the crime
    print("God to P: ")
    Prosecutor0_input = Prosecutor0_prefix + policy + item
    print(Prosecutor0_input)
    print("Prosecutor0: ")
    Prosecutor0_response = ask_model(Prosecutor0_input)
    print(Prosecutor0_response)
    print("-----------------------------------------------")
    #strip possible markdown format
    Prosecutor0_response = Prosecutor0_response.strip("``` json")
    Prosecutor0_response = Prosecutor0_response.strip("```json")
    Prosecutor0_response = Prosecutor0_response.strip("```")
    try:
        json_response = json.loads(Prosecutor0_response)
    except json.JSONDecodeError:
        print("Invalid JSON response from Prosecutor0.")
        return 0
    
    decision, explanation = json_response.get("decision"), json_response.get("explanation")
    if not ("yes" in decision):
        return 0
    
    # 3. Start the debate
    Scene = f"Here are the records of the court. <suspected Privacy Policy> {policy} </suspected Privacy Policy> <violated GDPR item> {item} </violated GDPR item>  <Sentence Reason> {explanation} </Sentence Reason>"
    for i in range(debate_iter):
        if(i % 2 == 0):
            print("God to L: ")
            Lawyer_input = Lawyer_prefix + Scene
            print(Lawyer_input)
            print("Lawyer: ")
            Lawyer_response = ask_model(Lawyer_input)
            print(Lawyer_response)
            print("-----------------------------------------------")
        else:
            print("God to P: ")
            Prosecutor1_input = Prosecutor1_prefix + Scene
            print(Prosecutor1_input)
            print("Prosecutor1: ")
            Prosecutor1_response = ask_model(Prosecutor1_input)
            print(Prosecutor1_response)
            print("-----------------------------------------------")
            
            
        if i == 0:
            Scene = Scene + "\n\n Debate: \n\n" 
        
        if i % 2 == 0:
            Scene = Scene + "<Lawyer>" + Lawyer_response + "</Lawyer>" + "\n\n"
        else:
            Scene = Scene + "<Prosecutor>" + Prosecutor1_response + "</Prosecutor>" + "\n\n"
            
    # 4. Judge the case
    print("God to J: ")
    Judge_input = Judge_prefix + Scene
    print(Judge_input)
    print("Judge: ")
    Judge_response = ask_model(Judge_input)
    print(Judge_response)
    print("-----------------------------------------------")
    #strip possible markdown format
    Judge_response = Judge_response.strip("``` json")
    Judge_response = Judge_response.strip("```json")
    Judge_response = Judge_response.strip("```")
    try:
        json_response = json.loads(Judge_response)
    except json.JSONDecodeError:
        print("Invalid JSON response from Judge.")
        return 0
    
    jdecision, jexplanation = json_response.get("decision"), json_response.get("explanation")
    if not ("guilty" in jdecision):
        return 0
    return 1
    
    
    
    
    
    
