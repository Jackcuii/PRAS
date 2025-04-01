import re

with open("privacy_policy/policies_googlePlay/Amazon Photos.txt", "r", encoding="utf-8") as file:
    content1 = file.read()
with open("privacy_policy/policies_googlePlay/Bilibili - HD Anime Videos.txt", "r", encoding="utf-8") as file:
    content2 = file.read()
with open("privacy_policy/policies_googlePlay/CityMall Online Shopping App.txt", "r", encoding="utf-8") as file:
    content3 = file.read()
    
    
def advanced_smart_split(text, delimiters):
    # 定义需要保护的缩写模式
    protected_patterns = {
        # 常见缩写
        r'i\.e\.': 'i.e.',
        r'e\.g\.': 'e.g.',
        r'etc\.': 'etc.',
        r'vs\.': 'vs.',
        
        # 称谓
        r'Mr\.': 'Mr.',
        r'Mrs\.': 'Mrs.',
        r'Ms\.': 'Ms.',
        r'Dr\.': 'Dr.',
        r'Prof\.': 'Prof.',
        
        # 时间相关
        r'a\.m\.': 'a.m.',
        r'p\.m\.': 'p.m.',
        
        # 国家/地区
        r'U\.S\.': 'U.S.',
        r'U\.K\.': 'U.K.',
        r'E\.U\.': 'E.U.',
        
        # 历史时期
        r'B\.C\.': 'B.C.',
        r'A\.D\.': 'A.D.',
        
        # 其他常见缩写
        r'Inc\.': 'Inc.',
        r'Ltd\.': 'Ltd.',
        r'Corp\.': 'Corp.',
        r'Co\.': 'Co.',
    }
    
    # 创建临时替换字典
    temp_dict = {}
    protected_text = text
    
    # 替换所有保护模式
    for pattern, replacement in protected_patterns.items():
        matches = re.finditer(pattern, protected_text)
        for i, match in enumerate(matches):
            temp_key = f'PROTECTED_{i}'
            temp_dict[temp_key] = match.group(0)
            protected_text = protected_text.replace(match.group(0), temp_key)
    
    # 按分隔符分割
    parts = re.split(f'[{delimiters}]', protected_text)
    
    # 还原被保护的模式
    result = []
    for part in parts:
        for temp_key, original in temp_dict.items():
            part = part.replace(temp_key, original)
        result.append(part.strip())
    
    return result



# split content with '.' or '\n'
inputs1 = advanced_smart_split(content1, '.\n')
inputs2 = advanced_smart_split(content2, '.\n')
inputs3 = advanced_smart_split(content3, '.\n')

# remove empty strings
inputs1 = [input for input in inputs1 if len(input.split(' ')) > 6]
inputs2 = [input for input in inputs2 if len(input.split(' ')) > 6]
inputs3 = [input for input in inputs3 if len(input.split(' ')) > 6]

# write to file
with open("AmazonPhotos_processed_original.txt", "w", encoding="utf-8") as file:
    for input in inputs1:
        file.write(input + '\n')
with open("BilibiliHDAnimeVideos_processed_original.txt", "w", encoding="utf-8") as file:
    for input in inputs2:
        file.write(input + '\n') 
with open("CityMallOnlineShoppingApp_processed_original.txt", "w", encoding="utf-8") as file:
    for input in inputs3:
        file.write(input + '\n') 

