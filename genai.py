from google import genai
import io,os
import httpx, pathlib, patch,shutil
from pydantic import BaseModel, TypeAdapter

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
thisFilePath = os.path.dirname(os.path.realpath(__file__))

folderPath = "AiEngine-main"
labelling_folder = os.path.join(thisFilePath, "labelling_files")

# 创建 labelling_files 文件夹，如果它不存在
if not os.path.exists(labelling_folder):
    os.makedirs(labelling_folder)

files = []
def push_labeled_file(file_path):
    new_file_path = os.path.join(labelling_folder, file_path.name)
    shutil.copy2(file_path, new_file_path) # 复制文件
    
    # 读取文件内容并插入行号
    with open(file_path, "r", encoding="utf-8") as f_in, open(new_file_path, "w", encoding="utf-8") as f_out:
        for i, line in enumerate(f_in):
            f_out.write(f"<line {i+1}> {line}<end of line {i+1}>\n")
    files.append(pathlib.Path(new_file_path))

for file in os.listdir(os.path.join(thisFilePath, folderPath,"templates")):
    filename = os.path.join(folderPath,"templates", os.fsdecode(file))
    if filename.endswith(".html"):
        push_labeled_file(pathlib.Path(filename))
        

for file in os.listdir(os.path.join(thisFilePath, folderPath, "static")):
    filename = os.path.join(folderPath,"static", os.fsdecode(file))
    if filename.endswith(".css"):
        file_path = pathlib.Path(filename)
        push_labeled_file(file_path)

files_prompt = []
for file_path in files:
    files_prompt.append(
        client.files.upload(
            file = file_path,
            config = dict(mime_type = "text/html" if file_path.suffix == ".html" else "text/css")
        )
    )

class Change(BaseModel):
    start: int # start line number
    end: int # end line number
    content: str # new content
    action: str # insert or remove

class Changes(BaseModel):
    filename: str
    changes: list[Change]
    
meta_args = dict(files = [str(file) for file in files])
meta_prompt = """
The HTML and CSS file is the source code of a website. You will be given a task to modify the website.
The task will be given in the form of natural language. Your should first separate the task into individual subtasks.
Your goal is to generate a modified version of the website that satisfies the task description.
You do not need to return the subtask generated or the breakdown of the task.
You only need to generate the JSON to indicate the changes on the HTML and CSS files provided. 

Use this JSON schema:
The filename is the name of the file that you want to change (you must use the file name of the files provided). The changes is a list of changes that you want to make to the file. Each change is a dictionary with the following keys:
- start: the start line number of the change
- end: the end line number of the change
- content: the new content
- action: insert or remove or replace

A bad example of a change is:
To change a row of buttons from positioned at center to positioned at left, a bad change is:
[{{\"filename\": \"music.css\", \"changes\": [{{\"start\": 17, \"end\": 18, \"content\": \"justify-content: left;\", \"action\": \"replace\"}}]}}]
where the content is
<line 17>    display: flex;
<end of line 17>
<line 18>    justify-content: center;
<end of line 18>
Because this change forgets that after the replacement, \"display: flex;\" is deleted. The correct change should be:
[{{\"filename\": \"music.css\", \"changes\": [{{\"start\": 18, \"end\": 18, \"content\": \"justify-content: left;\", \"action\": \"replace\"}}]}}]
Where it only replaces the line that needs to be replaced.


available file names are:
{files}
""".format(**meta_args).strip()

# prompt = "Change background color to blue. Change title to \"MYMUSICPLAYER\"".strip()
# prompt = "Change the music.css such that the background color of the website is blue. Change title in music.html file such that title of the webpage becomes \"MYMUSICPLAYER\"".strip()
# prompt = "Change the music.css such that the disk will not be rotating".strip()
# prompt = "Change the music.css such that the disk will not be rotating. Change the music.html such that the title of the webpage is \"MYMUSICPLAYER\"".strip()

prompt = "Look at the row of buttons containing play button, I want buttons of this row to be positioned at left, not spanning the whole width of the page".strip()

print([meta_prompt] + [prompt])


response = client.models.generate_content(
  model="gemini-1.5-flash",
  contents=files_prompt + [meta_prompt] + [prompt],
  config={
        'response_mime_type': 'application/json',
        'response_schema': list[Changes]
  }
)
print('')
print(response.text)
with open("test_webpage/output.json", "w+") as f:
    f.write(response.text)
