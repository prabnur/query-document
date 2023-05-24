import json
from post_process import group_by_table, table_data_to_csv, join_paragraphs


def json_print(data):
    print(json.dumps(data, indent=2))


def test_join_paragraphs():
    json_print(
        join_paragraphs(
            [
                {"path": "/P", "text": "dw kk"},
                {"path": "/P[2]", "text": "sdck."},
                {"path": "/P[3]", "text": "kcks. s dck."},
                {"path": "/P[4]", "text": "cnkcsn. alk cmk"},
                {"path": "/P[5]", "text": " cdn"},
                {"path": "/P[6]", "text": "sdck."},
            ]
        )
    )


def test_group_by_table():
    result = group_by_table(
        [
            {"path": "/Table/TR/TH/P", "text": "Charac"},
            {"path": "/Table/TR/TH[2]/P", "text": "mean QI0 dB "},
            {"path": "/Table/TR[2]/TD/P", "text": "0.5-1 "},
            {"path": "/Table/TR[2]/TD[2]/P", "text": "1.88 "},
            {"path": "/Table/TR[3]/TD/P", "text": "> 1-2 "},
            {"path": "/Table/TR[3]/TD[2]/P", "text": "2.39 "},
            {"path": "/Table[3]/TR/TH/P", "text": "Cha"},
            {"path": "/Table[3]/TR/TH[2]/P", "text": "SJU"},
            {"path": "/Table[3]/TR[2]/TD/P", "text": "29"},
            {"path": "/Table[3]/TR[2]/TD[2]/P", "text": "2.32"},
            {"path": "/Table[3]/TR[3]/TD/P", "text": "15"},
            {"path": "/Table[3]/TR[3]/TD[2]/P", "text": "2.39"},
            {"path": "/Table[6]/TR/TH/P", "text": "Cha"},
            {"path": "/Table[6]/TR/TH[2]/P", "text": "SJU"},
            {"path": "/Table[6]/TR[2]/TD/P", "text": "29"},
            {"path": "/Table[6]/TR[2]/TD[2]/P", "text": "2.32"},
            {"path": "/Table[6]/TR[3]/TD/P", "text": "15"},
            {"path": "/Table[6]/TR[3]/TD[2]/P", "text": "2.39"},
        ]
    )
    json_print(result)


def test_table_data_to_csv():
    result = table_data_to_csv(
        [
            {"path": "/Table/TR/TH/P", "text": "Characteristic frequency (kHz) "},
            {"path": "/Table/TR/TH[2]/P", "text": "mean QI0 dB "},
            {"path": "/Table/TR/TH[3]/P", "text": "SD "},
            {"path": "/Table/TR[2]/TD/P", "text": "0.5-1 "},
            {"path": "/Table/TR[2]/TD[2]/P", "text": "1.88 "},
            {"path": "/Table/TR[2]/TD[3]/P", "text": "0.53 "},
            {"path": "/Table/TR[3]/TD/P", "text": "> 1-2 "},
            {"path": "/Table/TR[3]/TD[2]/P", "text": "2.39 "},
            {"path": "/Table/TR[3]/TD[3]/P", "text": "0.54 "},
            {"path": "/Table/TR[4]/TD/P", "text": "> 2-4 "},
            {"path": "/Table/TR[4]/TD[2]/P", "text": "3.01 "},
            {"path": "/Table/TR[4]/TD[3]/P", "text": "0.86 "},
            {"path": "/Table/TR[5]/TD/P", "text": "> 4-8 "},
            {"path": "/Table/TR[5]/TD[2]/P", "text": "6.56 "},
            {"path": "/Table/TR[5]/TD[3]/P", "text": "1.79 "},
            {"path": "/Table/TR[6]/TD/P", "text": "> 8-16 "},
            {"path": "/Table/TR[6]/TD[2]/P", "text": "7.35 "},
            {"path": "/Table/TR[6]/TD[3]/P", "text": "2.45 "},
            {"path": "/Table/TR[7]/TD/P", "text": "> 16-32 "},
            {"path": "/Table/TR[7]/TD[2]/P", "text": "7.08 "},
            {"path": "/Table/TR[7]/TD[3]/P", "text": "2.5 "},
        ]
    )
    json_print(result)
