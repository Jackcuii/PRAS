__package__ = 'pras'

from transformers import AutoModelForCausalLM, AutoTokenizer


model = None
tokenizer = None
# 修改为本地模型路径
local_model_path = "./law-LLM"  # 假设模型存储在当前目录下的 law-LLM 文件夹中

# 从本地加载模型和分词器
def load_model():
    global model 
    model = AutoModelForCausalLM.from_pretrained(local_model_path)
    global tokenizer 
    tokenizer = AutoTokenizer.from_pretrained(local_model_path, use_fast=False)


user_input = '''Question: Which of the following is false about ex post facto laws?
    Options:
    - They make criminal an act that was innocent when committed.
    - They prescribe greater punishment for an act than was prescribed when it was done.
    - They increase the evidence required to convict a person than when the act was done.
    - They alter criminal offenses or punishment in a substantially prejudicial manner for the purpose of punishing a person for some past activity.

    Please provide your choice first and then provide explanations if possible.'''
    
    
# Put your input here:
def ask_model(user_input): 

    # Simply use your input as the prompt for base models
    prompt = user_input
    
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).input_ids.to(model.device)
    outputs = model.generate(input_ids=inputs, max_length=2048)[0]

    answer_start = int(inputs.shape[-1])
    pred = tokenizer.decode(outputs[answer_start:], skip_special_tokens=True)

    print(pred)
