import pandas as pd
import json
import requests

# with open("privacy_policy/policies_googlePlay/AnyDesk Remote Desktop.txt", "r", encoding="utf-8") as file:
#     content = file.read()

with open("privacy_policy/policies_googlePlay/Bilibili - HD Anime Videos.txt", "r", encoding="utf-8") as file:
#  with open("privacy_policy/policies_googlePlay/Amazon Photos.txt", "r", encoding="utf-8") as file:
# with open("privacy_policy/policies_googlePlay/CityMall Online Shopping App.txt", "r", encoding="utf-8") as file:
    content = file.read()

# cut lines
content = content.split('\n')
content = [line for line in content if len(line.split(' ')) > 5 ]
content = '\n'.join(content)
# with open("privacy_policy/policies_googlePlay/CityMall Online Shopping App.txt", "r", encoding="utf-8") as file:
#    content = file.read()

#
#    content = file.read()

# get the first 50000 characters
#if len(content) > 20000:
    #content = content[:20000]

with open("BilibiliHDAnimeVideos_processed_original.txt", "w", encoding="utf-8") as file:
    file.write(content)


def ask_llm(message):
    url = "https://api.theb.ai/v1/chat/completions"
    ctnt = "Try to divide (or combine) the whole text into lines. Each line should only be one complete sentence. i.e. If there is any line is only one isolate word of phrase (for example, the titles of the original text), you can just delete them. only give me the result, do not add any extra information. mark the end of each line with tag string \'</next>\' Remember you must try your best to include all the sentences in the original text. \n Target text: "
    payload = json.dumps({"model": "gpt-4o","messages": [{"role": "system","content": ctnt}, {"role": "user", "content": message}],"stream": False})
    headers = {
        'Authorization': 'Bearer sk-SCTZF4w8GFy07tpgmJDPVGhlQi5BSQA4tusj4TtW9oDK47gK',
        'Content-Type': 'application/json'
    }
    #print("Request sent")
    response = requests.request("POST", url, headers=headers, data=payload)
    print("Get response")
    print(response.text)
    jsonized = response.json()
    try:
        ret = jsonized["choices"][0]["message"]["content"]
    except json.decoder.JSONDecodeError or KeyError:
        print("Error:")
        print(jsonized)
        print("-----------------------------------")
    return ret

# concat into one string

ret = ask_llm(content)

# cut by </n> and   dump to txt
# with open("AnyDeskRemoteDesktop_processed.txt", "w", encoding="utf-8") as file:
#with open("BilibiliHDAnimeVideos_processed.txt", "w", encoding="utf-8") as file:
# with open("CityMallOnlineShoppingApp_processed.txt", "w", encoding="utf-8") as file:
with open("AmazonPhotos_processed.txt", "w", encoding="utf-8") as file:
    for line in ret:
        # do not append \n when writing to file
        file.write(line+'\n')
    