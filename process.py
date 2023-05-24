from ProcessPDF.extract import extract_pdf
from ProcessPDF.post_process import post_process

import zipfile
import json
import os


def process(dir, file):
    if not os.path.exists("./output"):
        os.makedirs("./output")

    # Adobe extract
    file_name_only = file.split(".")[0]
    json_path = os.path.join("./output", f"{file_name_only}.json")
    if not os.path.exists(json_path):
        print("I RAN, LOSE MONEY BITCH")
        output_file_path = f"./output/{file_name_only}.zip"
        extract_pdf(dir, file, output_file_path)

        # unzip
        with zipfile.ZipFile(output_file_path, "r") as zip_ref:
            zip_ref.extractall("./output")

        # rename
        os.rename(os.path.join("./output", "structuredData.json"), json_path)

    data = {}
    # Read the JSON file
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    if "elements" in data:
        return post_process(data["elements"])
    return {}
