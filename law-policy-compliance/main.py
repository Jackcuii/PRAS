import html2txt
import segment
dp = [6,7,22,38,41,49,56,61,62,65,80,82,90,93,101,102,104,105,110,111,112,139,192,210,215,218,223,225,238,248]

for i in dp:
    html2txt.convert_html_to_text(f"./dataset/original/{i}.html", f"./dataset/text/{i}.txt")
    segment.segment(f"./dataset/text/{i}.txt", f"./dataset/seged/{i}.txt")

# 线索化数据 就是把各级标题一直贯穿下来.

# 缺少数据

policy = ""
item = ""

policy = "<privacy policy>" + policy + "</privacy policy>"
item = "<GDPR item>" + item + "</GDPR item>"

Investigator0 = "You are an Investigator. Here is a part of an App's User Privacy Policy. Read the Private Policy and figure out whether it is possible to violates the GDPR. Just tell me \"yes\" (may violate) or \"no\" (non-violation). Do not tell me anything else. "
Investifator0 = Investigator0 + policy
Investigator1 = "You are an Investigator. Here is a part of an App's User Privacy Policy. Read the Private Policy and figure out whether it is related to the given GDPR item. Just tell me \"yes\" (related) or \"no\" (non-related). Do not tell me anything else. "
Investigator1 = Investigator1 + item
Prosecutor0 = "You are a Prosecutor in the court who is going to sentence a company by violating GDPR. The offcials collected some evidences. You are going to read the given privacy policy piece and the given GDPR item. Then decide whether to sentence the company for breaking the given article. You should answer me with \{ \"decision\" : \"yes\"/\"no\" , \"explanation\": ...\}"
Prosecutor0 = Prosecutor0 + policy + item

Scene = "The prosecutor is going to sentence the company, for their privacy policy violates the GDPR article. The prosecutor is going to read the privacy policy and the GDPR item. Then decide whether to sentence the company for breaking the given article. You should answer me with \{ \"decision\" : \"yes\"/\"no\" , \"explanation\": ...\}" 