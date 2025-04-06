import html2txt
import segment
dp = [6,7,22,38,41,49,56,61,62,65,80,82,90,93,101,102,104,105,110,111,112,139,192,210,215,218,223,225,238,248]

for i in dp:
    html2txt.convert_html_to_text(f"./dataset/original/{i}.html", f"./dataset/text/{i}.txt")
    segment.segment(f"./dataset/text/{i}.txt", f"./dataset/seged/{i}.txt")

# 线索化数据 就是把各级标题一直贯穿下来.

# 缺少数据

debate_iter = 6

policy = ""
item = ""

policy = "<privacy policy>" + policy + "</privacy policy>"
item = "<GDPR item>" + item + "</GDPR item>"

Investigator0_prefix = "You are an Investigator. Here is a part of an App's User Privacy Policy. Read the Private Policy and figure out whether it is possible to violates the GDPR. Just tell me \"yes\" (may violate) or \"no\" (non-violation). Do not tell me anything else. "
Investigator1_prefix = "You are an Investigator. Here are a piece of an App's User Privacy Policy and a GDPR article. Read the Private Policy and figure out whether it is related to the given GDPR article. Just tell me \"yes\" (related) or \"no\" (non-related). Do not tell me anything else. "

Prosecutor0_prefix = "You are a Prosecutor in the court who is going to sentence a company by violating GDPR. The offcials collected some evidences. You are going to read the given privacy policy piece and the given GDPR item. Then decide whether to sentence the company for breaking the given article. You should answer me with \{ \"decision\" : \"yes\"/\"no\" , \"explanation\": ...\}"
Lawyer = "You are a Defense Lawyer in the court who is going to defend a company from being sentenced by violating GDPR. You should try to dispute the prosecutor's statements and be inherent with you own past statements. "
Scene = f"Here are the records of the court. <suspected Privacy Policy> {policy} </suspected Privacy Policy> <violated GDPR item> {item} </violated GDPR item> <Investigator0> {Investigator0} </Investigator0> <Investigator1> {Investigator1} </Investigator1> <Prosecutor0> {Prosecutor0} </Prosecutor0> <Lawyer> {Lawyer} </Lawyer>"
Judge = ""

def start_court():
    pass

def start_judgement(policy, item):
    # 1. search evidences
    print("God to I0: ")
    Investigator0_input = Investigator0_prefix + policy
    print(Investigator0_input)
    print("Investigator0: ")
    Investigator0_response = ask_model(Investigator0_input)
    print(Investigator0_response)
    if not ("yes" in Investigator0_response):
        return 0
    
    print("God to I1: ")
    Investigator1_input = Investigator1_prefix + policy + item
    print(Investigator1_input)
    print("Investigator1: ")
    Investigator1_response = ask_model(Investigator1_input)
    print(Investigator1_response)
    if not ("yes" in Investigator1_response):
        return 0
    
    # 2. identify the crime
    print("God to P: ")
    Prosecutor0_input = Prosecutor0_prefix + policy + item
    
    
    
    
        
        
    ask_model(Investigator0)
    
    
    
    
    
