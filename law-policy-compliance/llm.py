__package__ = 'pras'

from transformers import AutoModelForCausalLM, AutoTokenizer


local_run = False

model = None
tokenizer = None

def load_model():
    if local_run:
        global model 
        model = AutoModelForCausalLM.from_pretrained("AdaptLLM/law-chat").to("cuda")
        global tokenizer 
        tokenizer = AutoTokenizer.from_pretrained("AdaptLLM/law-chat")
    else:
        print("API running")

# Put your input here:

def ask_remote_model(user_input):
    
    from openai import OpenAI
    client = OpenAI(api_key="sk-c1248ef96b7f4f7c8db7ca74fd06f054", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": user_input}
        ],
        stream=False
    )
    return response.choices[0].message.content


def ask_model(user_input): 


    # Simply use your input as the prompt for base models
    
    # system_prompt = "\nYou are an assistant. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n" 
    if local_run:
        system_prompt = ""
        prompt = f"<s>[INST] <<SYS>>{system_prompt}<</SYS>>\n\n{user_input} [/INST]"

        inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).input_ids.to(model.device)
        outputs = model.generate(input_ids=inputs, max_length=4096)[0]
        
        
        answer_start = int(inputs.shape[-1])
        pred = tokenizer.decode(outputs[answer_start:], skip_special_tokens=True)
        
        return pred
    else:
        return ask_remote_model(user_input)

