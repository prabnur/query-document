import re

TEXT_FILTERS = [
    # number
    r"^[0-9]*$",
    # figure eg. "Fig 4D"
    r"^Fig[.]? [0-9a-fA-F]+$",
    # dot
    r"^[.]$",
    # Starts with https://
    r"^https://.*$",
    # Starts with http://
    r"^http://.*$",
    # single letter (captial or lowercase)
    r"^[a-zA-Z]$",
]

PATH_FILTERS = [r"^.*/Aside.*$"]

TEXT_SUBSTITUTIONS = [
    ("\u00ad", "-"),
    ("\u2013", "-"),
    ("\u2014", "-"),
    ("\u00a0", " "),
    ("\u200b", ""),
    ("\u200c", ""),
    ("\u200d", ""),
    ("\u201c", '"'),
    ("\u201d", '"'),
    ("\u2018", "'"),
    ("\u2019", "'"),
]


def substitute(text):
    for pattern, replacement in TEXT_SUBSTITUTIONS:
        text = text.replace(pattern, replacement)
    return text


def filter(S, patterns):
    return any([re.match(pattern, S.strip()) for pattern in patterns])


def remove_prefix(text):
    return text.replace("//Document", "")


def is_figure_text(text):
    return re.match(r"^Fig[.]? [0-9]+[a-zA-Z]*[.]?.*$", text)


def is_heading(path):
    return re.match(r".*/H[1-9].*$", path)


def is_paragraph(path):
    return re.match(r".*/P\[\d+\].*$", path)


def table_data_to_csv(table_data):
    # Initialize a dictionary to store row index and corresponding data
    data_dict = {}

    # Regex pattern for extracting the row and column index from the path
    pattern = re.compile(r"/Table/TR(\[\d+\])?/(TH|TD)(\[\d+\])?/P")

    for record in table_data:
        match = pattern.match(record["path"])
        if match:
            # Default row and column index is 1 if not specified
            row_idx = int(match.group(1)[1:-1]) if match.group(1) else 1
            col_idx = int(match.group(3)[1:-1]) if match.group(3) else 1

            if row_idx not in data_dict:
                data_dict[row_idx] = {}

            data_dict[row_idx][col_idx] = record["text"]

    # Convert the dictionary to a list of lists sorted by row index
    sorted_data = [
        [row[col_idx] for col_idx in sorted(row)]
        for row in [data_dict[row_idx] for row_idx in sorted(data_dict)]
    ]

    # Convert the data to a CSV format
    # csv_data = "\n".join([",".join(row) for row in sorted_data])
    # return [",".join(row) for row in sorted_data]

    return sorted_data


def join_spans(data):
    consolidated = {}
    for item in data:
        # Get base path without ParagraphSpan
        path = item["path"].split("/ParagraphSpan")[0]

        # If base path is not in consolidated, add it
        if path not in consolidated:
            consolidated[path] = item["text"]
        # If base path is in consolidated, append the text
        else:
            consolidated[path] += item["text"]

    # Convert consolidated dictionary to list of dictionaries
    consolidated_list = [
        {"path": path, "text": text} for path, text in consolidated.items()
    ]

    return consolidated_list


def join_paragraphs(data):
    consolidated = []
    new_para_idx = 2
    last_open_para_idx = -1

    def is_closed_paragraph(text):
        return re.match(r".*[.]$", text.strip())

    def new_para_path(path):
        return re.sub(r"/P\[\d+\]", f"/P[{new_para_idx}]", path)

    def append_last_open_para(text):
        consolidated[last_open_para_idx]["text"] += text

    for element in data:
        path = element["path"]
        text = element["text"]
        if not is_paragraph(path):
            consolidated.append(element)
            last_open_para_idx = -1
            continue
        if last_open_para_idx == -1:
            consolidated.append({"path": new_para_path(path), "text": text})
            new_para_idx += 1
            if not is_closed_paragraph(text):
                last_open_para_idx = len(consolidated) - 1
        else:
            append_last_open_para(text)
            if is_closed_paragraph(text):
                last_open_para_idx = -1

    return consolidated


def group_by_table(input_data):
    grouped_data = {}
    for item in input_data:
        # Get table number from the path
        match = re.search(r"/Table\[(\d+)\]", item["path"])
        table_number = match.group(1) if match else "1"

        # If table number is not in grouped_data, add it
        if table_number not in grouped_data:
            grouped_data[table_number] = []

        # Modify the path to remove the table number and add the item to the list
        item["path"] = re.sub(r"/Table\[(\d+)\]", "/Table", item["path"])
        grouped_data[table_number].append(item)

    # Convert grouped_data dictionary to list of lists
    output_data = list(grouped_data.values())

    return output_data


def post_process(elements):
    content = []
    others = []
    tables = []
    refernces = []
    ADD_REFERNCES = False
    for element in elements:
        if "Text" not in element:
            continue

        text = substitute(element["Text"])
        path = remove_prefix(element["Path"])
        if filter(text, TEXT_FILTERS) or filter(path, PATH_FILTERS):
            continue
        data = {"path": path, "text": text}

        if "/Reference" in path:
            others.append(data)
        elif "/Table" in path:
            tables.append(data)
        elif is_heading(path) or is_paragraph(path) or "/Title" in path:
            if is_heading(path) and "References" in text:
                ADD_REFERNCES = True
                continue

            if is_figure_text(text):
                others.append(data)
            elif ADD_REFERNCES:
                if is_paragraph(path):
                    refernces.append(text)
            else:
                content.append(data)

    # Tables
    tables = group_by_table(tables)
    tables = list(map(table_data_to_csv, tables))

    # Content
    content = join_spans(content)
    content = join_paragraphs(content)

    new_data = {
        "content": content,
        "others": others,
        "tables": tables,
        "references": refernces,
    }
    return new_data
    # Write the data to a JSON file
    # with open("structuredDataProcessed.json", "w") as outfile:
    #     json.dump(new_data, outfile)
