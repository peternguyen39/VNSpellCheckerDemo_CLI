import json
from os import mkdir

def parseJSON(file):
    try:
        mkdir("data")
    except FileExistsError:
        pass
    with open(file, 'r',encoding="utf-8") as f:
        for i in f:
            json_data = json.loads(i)
            fileName = json_data['_id']
            with open("data/"+fileName+".txt", 'w',encoding="utf-8") as fout:
                fout.write(json_data["text"])
                fout.close()
        f.close()

parseJSON('spelling_test.json')
            