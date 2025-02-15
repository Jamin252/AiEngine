import os
from openai import OpenAI

client = OpenAI()

META_PROMPT = """
Given a task description or existing prompt, produce a detailed system prompt to guide a language model in completing the task effectively.

# Guidelines

- Understand the Task: Grasp the main objective, goals, requirements, constraints, and expected output.
- Minimal Changes: If an existing prompt is provided, improve it only if it's simple. For complex prompts, enhance clarity and add missing elements without altering the original structure.
- Reasoning Before Conclusions**: Encourage reasoning steps before any conclusions are reached. ATTENTION! If the user provides examples where the reasoning happens afterward, REVERSE the order! NEVER START EXAMPLES WITH CONCLUSIONS!
    - Reasoning Order: Call out reasoning portions of the prompt and conclusion parts (specific fields by name). For each, determine the ORDER in which this is done, and whether it needs to be reversed.
    - Conclusion, classifications, or results should ALWAYS appear last.
- Examples: Include high-quality examples if helpful, using placeholders [in brackets] for complex elements.
   - What kinds of examples may need to be included, how many, and whether they are complex enough to benefit from placeholders.
- Clarity and Conciseness: Use clear, specific language. Avoid unnecessary instructions or bland statements.
- Formatting: Use markdown features for readability. DO NOT USE ``` CODE BLOCKS UNLESS SPECIFICALLY REQUESTED.
- Preserve User Content: If the input task or prompt includes extensive guidelines or examples, preserve them entirely, or as closely as possible. If they are vague, consider breaking down into sub-steps. Keep any details, guidelines, examples, variables, or placeholders provided by the user.
- Constants: DO include constants in the prompt, as they are not susceptible to prompt injection. Such as guides, rubrics, and examples.
- Output Format: Explicitly the most appropriate output format, in detail. This should include length and syntax (e.g. short sentence, paragraph, JSON, etc.)
    - For tasks outputting well-defined or structured data (classification, JSON, etc.) bias toward outputting a JSON.
    - JSON should never be wrapped in code blocks (```) unless explicitly requested.

The final prompt you output should adhere to the following structure below. Do not include any additional commentary, only output the completed system prompt. SPECIFICALLY, do not include any additional messages at the start or end of the prompt. (e.g. no "---")

[Concise instruction describing the task - this should be the first line in the prompt, no section header]

[Additional details as needed.]

[Optional sections with headings or bullet points for detailed steps.]

# Steps [optional]

[optional: a detailed breakdown of the steps necessary to accomplish the task]

# Output Format

output Python code that produces the desired output

# Examples [optional]

[Optional: 1-3 well-defined examples with placeholders if necessary. Clearly mark where examples start and end, and what the input and output are. User placeholders as necessary.]
[If the examples are shorter than what a realistic example is expected to be, make a reference with () explaining how real examples should be longer / shorter / different. AND USE PLACEHOLDERS! ]

# Notes [optional]

[optional: edge cases, details, and an area to call or repeat out specific important considerations]
""".strip()
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
[HTML or CSS code]
---endfile [file name]
""".format(**meta_args)

# print(meta_prompt)

def give_meta():
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": meta_prompt,
            }
        ],
    )

    return completion.choices[0].message.content

def give_prompt(msg: str):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": msg,
            },
        ],
    )

    return completion.choices[0].message.content

give_meta()
with open("prompt.txt", "r") as f:
    p = f.read()
    # print(p)
    ans = give_prompt(p)
    with open("output1.txt", "w") as fout:
        fout.write(ans)
