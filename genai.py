from google import genai
import io,os
import httpx, pathlib, patch,shutil
from pydantic import BaseModel, TypeAdapter
from apply_patch import apply_patch

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
thisFilePath = os.path.dirname(os.path.realpath(__file__))

folderPath = "AiEngine-main"
labelling_folder = os.path.join(thisFilePath, "labelling_files")

def main(msg):

    if not os.path.exists(labelling_folder):
        os.makedirs(labelling_folder)

    files = []
    original_files = []
    def push_labeled_file(file_path):
        original_files.append(file_path)
        new_file_path = os.path.join(labelling_folder, file_path.name)
        shutil.copy2(file_path, new_file_path) 
        
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

    with open("secret_recipe.txt", "r") as f:
            secret_recipe = f.read().strip()
    meta_args = dict(files = [str(file) for file in original_files], secret_recipe = secret_recipe)
    meta_prompt = """
    The HTML and CSS file is the source code of a website. You will be given a task to modify the website. The task will be given in the form of natural language. Your should first separate the task into individual subtasks. You should then read through each file and get the line number for each line of code. Your goal is to generate a modified version of the website that satisfies the task description. You do not need to return the subtask generated or the breakdown of the task. You only need to generate the JSON to indicate the changes on the HTML and CSS files provided. 

    Use this JSON schema:
    The filename is the name of the file that you want to change (you must use the file name of the files provided). The changes is a list of changes that you want to make to the file. Each change is a dictionary with the following keys:
    - start: the start line number of the change (the content will be inserted after this line)
    - end: the end line number of the change (inclusive)
    - content: the new content
    - action: insert or remove or replace

    {secret_recipe}

    available file paths are:
    {files}

    You should follow the following rules when making changes to the HTML and CSS files:
    You should reset the line number when you switch to a new file.
    Your start and end line number should not exceed the total number of lines in the file.
    """.format(**meta_args).strip()
    # print(meta_args["files"])

    # prompt = "Change background color to blue. Change title to \"MYMUSICPLAYER\"".strip()
    # prompt = "Change the music.css such that the background color of the website is blue. Change title in music.html file such that title of the webpage becomes \"MYMUSICPLAYER\"".strip()
    # prompt = "Change the music.css such that the disk will not be rotating".strip()
    # prompt = "Change the music.css such that the disk will not be rotating. Change the music.html such that the title of the webpage is \"MYMUSICPLAYER\"".strip()

    prompt = "Look at the row of buttons containing play button, I want buttons of this row to be positioned at left, not spanning the whole width of the page".strip()

    # print([meta_prompt] + [prompt])


    response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=files_prompt + [meta_prompt] + [msg],
    config={
            'response_mime_type': 'application/json',
            'response_schema': list[Changes]
    }
    )
    # print('')
    # print(response.text)
    with open("output.json", "w+") as f:
        f.write(response.text)
        
    apply_patch("output.json")
    
main("Look at the row of buttons containing play button, I want buttons of this row to be positioned at left, not spanning the whole width of the page")