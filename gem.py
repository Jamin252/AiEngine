from google import genai
import os
import io


meta_args = {}

htmlFiles = """"""
for file in os.listdir("test_webpage"):
    filename = os.path.join("test_webpage", os.fsdecode(file))
    if filename.endswith(".html"):
        with open(filename, "r") as f:
            htmlFiles += f"---{file}\n" + f.read().strip() + "\n\n"
meta_args["HTMLFiles"] = htmlFiles

css_files = """"""
for file in os.listdir("test_webpage/css"):
    filename =  os.path.join("test_webpage/css", os.fsdecode(file))
    if filename.endswith(".css"):
        with open("test_webpage/css/jquery.css", "r") as f:
            css_files += f"---{file}\n" + f.read().strip() + "\n" + f"---endfile {file}"+"\n\n"
meta_args["CSSFiles"] = css_files

meta_prompt = """
You are given a list of HTML files and CSS files with the following format:
---[file name]
[HTML or CSS code]
---endfile [file name]

HTML files:
{HTMLFiles}

CSS files:
{CSSFiles}

The HTML and CSS file is the source code of a website. You will be given a task to modify the website. The task will be given in the form of natural language. Your should first separate the task into individual subtasks. Your goal is to generate a modified version of the website that satisfies the task description. You need to generate the all the HTML and CSS files provided. 
Example task description:
Change the background color of the website to blue.
Change the font size to 100
Change the font family to Arial
Change the font color to red

The output should be in the following format:
---[file name]
[patch file]
---endfile [file name]

where [patch file] is the modified HTML or CSS code, the format of the patch file should be:
---remove [line selector]
---insert [line number] [code]

example of patch file is:
---remove 3
---insert 3 <h1>Modified Heading</h1>

""".format(**meta_args)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-1.5-pro-exp-0827",
    contents=meta_prompt,
)

print(response.text)