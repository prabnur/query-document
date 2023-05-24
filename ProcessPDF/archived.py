from post_process import match_filters
import json
from collections import Counter

HEADING_SIZES = [12]
TEXT_SIZES = [8, 10]
MINIMUM_HEADING_LENGTH = 2

elements = []

def post_process():
    new_data = []
    for element in elements:
        if (
            ("TextSize" not in element)
            or ("Text" not in element)
            or (match_filters(element["Text"]))
        ):
            continue
        size = round(element["TextSize"])

        if size in HEADING_SIZES and len(element["Text"]) > MINIMUM_HEADING_LENGTH:
            new_data.append({"title": element["Text"], "texts": []})
        elif size in TEXT_SIZES:
            if len(new_data) != 0:
                new_data[-1]["texts"].append(element["Text"])
            else:
                new_data.append({"title": "Start", "texts": [element["Text"]]})

    with open("structuredDataProcessed.json", "w") as outfile:
        json.dump(new_data, outfile)

def count_sizes():
    sizes = []
    for element in elements:
        if "TextSize" not in element:
            continue
        sizes.append(round(element["TextSize"]))
    C = Counter(sizes)
    print(C)
