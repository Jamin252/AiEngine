import os
import re
from flask import Flask, Response

app = Flask(__name__)
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def render_template_custom(filename):
    template_path = os.path.join(TEMPLATE_DIR, filename)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        return f'<!-- Template file {filename} not found -->'
    
    # Match custom tags like <tagName/>
    pattern = re.compile(r'<(\w+)\s*/>')
    
    def replace_tag(match):
        tag_name = match.group(1)
        # Assume the related template file is tag_name.html
        replacement = render_template_custom(f'{tag_name}.html')
        return replacement
    
    # Replace all matched tags (recursive call)
    rendered = pattern.sub(replace_tag, content)
    return rendered

@app.route('/')
def index():
    html_content = render_template_custom('music.html')
    return Response(html_content, mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)