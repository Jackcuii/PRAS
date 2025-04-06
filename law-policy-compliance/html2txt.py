__package__ = "pras"

import html2text

def convert_html_to_text(html_file, target_file):
    # Read the HTML content from the file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Convert HTML to Markdown
    markdown_content = html2text.html2text(html_content)
    
    plain_text_content = markdown_content.replace('\n', ' ').replace('  ', ' ').strip()
    # Write the Markdown content to the target file

    with open(target_file, 'w', encoding='utf-8') as file:
        file.write(plain_text_content)
        
