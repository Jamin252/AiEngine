from google import genai
import io,os
import httpx, pathlib, patch
from pydantic import BaseModel, TypeAdapter

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
thisFilePath = os.path.dirname(os.path.realpath(__file__))

files = []
for file in os.listdir(os.path.join(thisFilePath, "test_webpage")):
    filename = os.path.join("test_webpage", os.fsdecode(file))
    if filename.endswith(".html"):
        with open(filename, "r") as f:
            files.append(pathlib.Path(filename))
for file in os.listdir(os.path.join(thisFilePath, "test_webpage", "css")):
    filename = os.path.join("test_webpage","css", os.fsdecode(file))
    if filename.endswith(".css"):
        with open(filename, "r") as f:
            files.append(pathlib.Path(filename))

files_prompt = []
for file_path in files:
    files_prompt.append(
        client.files.upload(
            file = file_path,
            config = dict(mime_type = "text/html" if file_path.suffix == ".html" else "text/css")
        )
    )
patch_file_exp = client.files.upload(file = pathlib.Path(os.path.join(thisFilePath, "test_webpage", "0001-ai-done.patch")), config = dict(mime_type = "text/plain"))
# meta_prompt = """
# The HTML and CSS file is the source code of a website. You will be given a task to modify the website. The task will be given in the form of natural language. Your should first separate the task into individual subtasks. Your goal is to generate a modified version of the website that satisfies the task description. You do not need to return the subtask generated or the breakdown of the task. You only need to generate the git patch file for the HTML and CSS file provided. 
# Example task description:
# Change the background color of the website to blue.
# Change the font size to 100
# Change the font family to Arial
# Change the font color to red

# The output should be a git patch file that contains the changes made to the HTML and CSS files.
# The example patch file is put in file 0001-ai-done.patch 
# """.strip()

class Change(BaseModel):
    start: int # start line number
    end: int # end line number
    content: str # new content
    action: str # insert or remove

class Changes(BaseModel):
    filename: str
    changes: list[Change]
    
meta_args = dict(files = [str(file.absolute()) for file in files])
meta_prompt = """
The HTML and CSS file is the source code of a website. You will be given a task to modify the website. The task will be given in the form of natural language. Your should first separate the task into individual subtasks. Your goal is to generate a modified version of the website that satisfies the task description. You do not need to return the subtask generated or the breakdown of the task. You only need to generate the JSON to indicate the changes on the HTML and CSS files provided. 
Example task description:
Change the background color of the website to blue.
Change the font size to 100
Change the font family to Arial
Change the font color to red

Use this JSON schema:
The filename is the name of the file that you want to change (you must use the file name of the files provided). The changes is a list of changes that you want to make to the file. Each change is a dictionary with the following keys:
- start: the start line number of the change
- end: the end line number of the change
- content: the new content
- action: insert or remove or replace

available file names are:
{files}
""".format(**meta_args).strip()
print(meta_prompt)
prompt = "Change background color to blue. change font size to 100. add a button name home at the bottom of the page. Change title to (changed header)".strip()

response = client.models.generate_content(
  model="gemini-1.5-flash",
  contents=files_prompt + [patch_file_exp] + [meta_prompt] + [prompt],
  config={
        'response_mime_type': 'application/json',
        'response_schema': list[Changes]
  }
)
print(response.text)
with open("test_webpage/output.json", "w+") as f:
    f.write(response.text)
