import html2txt
import segment
dp = [6,7,22,38,41,49,56,61,62,65,80,82,90,93,101,102,104,105,110,111,112,139,192,210,215,218,223,225,238,248]

for i in dp:
    # html2txt.convert_html_to_text(f"./dataset/original/{i}.html", f"./dataset/text/{i}.txt")
    segment.segment(f"./dataset/text/{i}.txt", f"./dataset/seged/{i}.txt")

    