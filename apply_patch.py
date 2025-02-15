import json,os
from pprint import pprint

current_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(current_path, "output.json"), "r") as f:
    patch = json.load(f)
    for filePatches in patch:
        pprint(filePatches["filename"])
        changes = filePatches["changes"]
        # pprint(changes)
        res = []
        with open(os.path.join(current_path, filePatches["filename"]), "r") as f:
            content = f.read().split("\n")
            res = []
            print(f"content == {content}")
            l = len(content)
            i = 1
            while i<= l:
                for change in changes:
                    # print(f"change {change["action"]}, {i}, {change["start"]}, {change["end"]}")
                    if change["action"] == "remove" and i == int(change["start"]):
                        while i < change["end"]:
                            i += 1
                        break
                    if change["action"] == "insert" and i == int(change["start"]):
                        res.append(content[i-1])
                        res.append(change["content"])
                        break
                    if change["action"] == "replace" and i == int(change["start"]):
                        res.append(change["content"])
                        while i < change["end"]:
                            i += 1
                        break
                else:
                    res.append(content[i-1])
                i += 1
            # print(res)
        with open(os.path.join(current_path, filePatches["filename"]), "w+") as f:
            f.write("\n".join(res))
