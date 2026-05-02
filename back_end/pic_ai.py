import json
from pathlib import Path

ordner = Path("./pictures/")
new_pics = []
old_pics = []

for files in ordner.iterdir():
    new_pics.append(files.name.removesuffix(".png"))

with open("./picture_search_file.json", "r") as f:
    search_file = json.load(f)

for picture_id, info in search_file.items():
    old_pics.append(info["file"])

for pic in new_pics:
    if not pic in old_pics:
        pic_id = len(search_file)
        new_pic = {
            "name" : None,
            "description" : None,
            "file" : pic,
            "id" : pic_id
        }
        print(1)
        search_file["id" + str(pic_id)] = new_pic

with open("./picture_search_file.json", "w") as f:
    json.dump(search_file, f, indent=2)
