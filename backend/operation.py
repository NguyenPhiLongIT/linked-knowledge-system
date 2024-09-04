from flask import request
from neo4j import GraphDatabase
from unidecode import unidecode
import re


def clean_title(title):
    # Giữ lại chữ cái (bao gồm dấu tiếng Việt), số và dấu cách
    return re.sub(
        r"[^\w\sàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]",
        " ",
        title,
    )


def format(text):
    """
    Chuyển đổi chuỗi tiếng Việt thành in hoa không dấu không cách.

    Args:
        text (str): Chuỗi đầu vào.

    Returns:
        str: Chuỗi đã chuyển đổi.
    """

    return unidecode(text).upper().replace(" ", "")


def f_re(relationship):
    relationship = " ".join(unidecode(relationship).lower().split())
    result = relationship[0].upper()
    for i in range(1, len(relationship)):
        if relationship[i - 1] == " ":
            result += relationship[i].upper()
        else:
            result += relationship[i]
    return unidecode(result).replace(" ", "")



def them(my_dict, relationship, parent_node):
    command = "CREATE(a:"
    proper = ""
    title = ""
    for key, value in my_dict.items():
        if key != "Title":
            proper += f', `{key}`: "{value}"'
        else:
            title = format(value)
            print("Title", title)
            proper = f'`{key}`: "{value}"' + proper

    proper = proper.lstrip(", ")
    command += f"{title} {{{proper}}})"
    re = f_re(relationship)
    connect_cmd = (
        "\nWITH a\n"
        + "MATCH (b:"
        + parent_node
        + ")\nCREATE (b)-[r:"
        + re
        + "]->(a)\nRETURN a, b, r"
    )
    # print(connect_cmd)
    combine = command + connect_cmd
    print("combine", combine)
    return combine


def sua(title, my_dict):
    proper = ""
    for key, value in my_dict.items():
        print("key:", key, "value:", value)
        if key != "Title":
            if value[0] != "[":
                proper = proper + "," + key + ':"' + value + '"'
            else:
                proper = proper + "," + key + ":" + value
            print("proper", proper)
    proper = 'Title:"' + title + '"' + proper
    command = 'MATCH (n) WHERE n.Title = "' + title + '"\n SET n = {'
    command = command + proper + "}\nRETURN n"
    return command


def xoa(title):
    command = 'MATCH (n) WHERE n.Title = "' + title + '"\nDETACH DELETE n'
    return command


def create_query(key, position):
    before = (
        'MATCH (startNode)-[r]->(endNode) WHERE "'
        + key
        + '" IN labels(endNode) RETURN startNode,r,endNode;'
    )
    after = (
        'MATCH (startNode)-[r]->(endNode) WHERE "'
        + key
        + '" IN labels(startNode) RETURN startNode,r,endNode;'
    )
    if position == 0:
        return before
    else:
        return after


def show():
    cmd = "MATCH (n)-[r]->(end)\nWHERE NOT ()-[]->(n)\nRETURN collect(DISTINCT n) as n,collect(DISTINCT end) as end"
    return cmd

def chunk_feature(str, arrPolarityTerm):
    # Maximum_Matching
    vTerm = []
    strRemain = ""
    start = 0
    isTerm = False
    isStop = False

    # str = str.lower()
    str = str.lstrip(" ").rstrip(" ")
    WordList = str.split(" ")
    stop = len(WordList)

    while isStop == False and stop >= 0:
        for num in range(start, stop):
            strRemain = strRemain + WordList[num] + " "

        strRemain = strRemain.lstrip(" ").rstrip(" ")
        isTerm = False
        for cha in range(0, len(arrPolarityTerm)):
            arr = arrPolarityTerm[cha]
            if arr == strRemain:
                vTerm.append(strRemain)
                isTerm = True
                if start == 0:
                    isStop = True
                else:
                    stop = start
                    start = 0

        if isTerm == False:
            if start == stop:
                stop = stop - 1
                start = 0
            else:
                start += 1

        strRemain = ""
    strRemain = ""
    for stt in range(0, len(vTerm)):
        strRemain = strRemain + " " + vTerm[stt]
        print("vTerm", strRemain)
    return vTerm


# def remove_extra_spaces(text):
#     return " ".join(text.split())
