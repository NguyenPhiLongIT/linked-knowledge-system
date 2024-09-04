from flask_cors import CORS
from neo4j import GraphDatabase
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import json
from unidecode import unidecode
from operation import (
    them,
    sua,
    xoa,
    create_query,
    show,
    format,
    chunk_feature,
    clean_title,
)

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "12345678")
dict = {
    "Concept": "Định nghĩa",
    "Example": "Ví dụ",
    "EnglishName": "Tên tiếng anh",
    "OtherName": "Tên gọi khác",
    "Title": "Tiêu đề",
}
arrPolarityTerm = []
driver = GraphDatabase.driver(URI, auth=AUTH)
app = Flask(__name__, static_folder="public", static_url_path="/public")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# # Đóng kết nối


CORS(app)


@app.route("/")
def home():
    global dict
    global arrPolarityTerm
    cmd = ""
    with driver.session() as session:
        result = session.run(show()).data()
        nodes = []
        for r in result:
            root = r["n"][0]
            # print(root)
            node_data = {
                "labels": format(root["Title"]),
                "Title": root["Title"],
                "Concept": root["Concept"],
            }
            print(node_data)
            nodes.append(node_data)
            node_child = r["end"]
            print(node_child)
            for i in range(0,len(node_child)):
                node_data = {
                    "labels": format(node_child[i]["Title"]),
                    "Title": node_child[i]["Title"],
                    "Concept": node_child[i]["Concept"],
                }
                nodes.append(node_data)
        titles = session.run("MATCH (n) RETURN n.Title AS Titles")
        for record in titles:
            title = record["Titles"]
            arrPolarityTerm.append(title)
    return render_template("index.html", dict=dict, nodes=nodes)


@app.route("/graph", methods=["GET"])
def list():
    global dict
    global arrPolarityTerm
    nodes = []
    edges = []
    with driver.session() as session:
        res_result = session.run(
            "MATCH (start)-[r]->(end) \nRETURN id(start) AS source, id(end) AS target"
        )
        for node in res_result:
            new_edge = {
                "source": "node" + str(node["source"]),
                "target": "node" + str(node["target"]),
            }
            edges.append(new_edge)
        nodes_result = session.run("MATCH (n)\nRETURN id(n) AS id, n.Title AS name")
        for node in nodes_result:
            new_node = {"id": node["id"], "name": node["name"]}
            nodes.append(new_node)
        print(len(nodes))
        print(len(edges))
    return jsonify({"nodes": nodes, "edges": edges})


@app.route("/search", methods=["POST"])
def search():
    global dict
    global arrPolarityTerm
    keyword = request.form.get("query")
    key = clean_title(request.form.get("query").upper())  # dùng cho nhiều keyword
    one_key = format(request.form.get("query"))
    print("one_key", one_key)
    nodes_list = []
    one_key_cmd = (
        'MATCH (n) WHERE any(label IN labels(n) WHERE label CONTAINS "'
        + one_key
        + '") RETURN n'
    )

    arr = chunk_feature(clean_title(key), arrPolarityTerm)
    formatted_string = json.dumps(arr, ensure_ascii=False)
    many_key_cmd = (
        "WITH "
        + formatted_string
        + "AS titles\n"
        + "MATCH (n) WHERE n.Title IN titles\nRETURN n"
    )

    with driver.session() as session:
        try:
            nodes = session.run(many_key_cmd)
            for record in nodes:
                node = record["n"]
                # Convert the node to a dictionary
                print("node", list(node.labels)[0])
                print(
                    "node._properties",
                    node._properties["Concept"],
                    node._properties["Title"],
                )
                node_data = {"labels": list(node.labels)[0], **node._properties}
                nodes_list.append(node_data)
            # if len(nodes_list) == 0:

        except Exception as e:
            print(f"Error: {e}")
            return jsonify(nodes_list=[])

    return render_template("search.html", dict=dict, query=keyword, results=nodes_list)
    # return jsonify(nodes_list=nodes_list)


@app.route("/create-node", methods=["POST"])
def create_node():
    my_dict = {}

    for key, value in request.form.items():
        if key not in [
            "property_name",
            "property_value",
            "Parent_Node",
            "Relationship",
        ]:
            my_dict[key] = value
    print("dict", my_dict)
    parent_node = request.form.get("Parent_Node")
    relationship = request.form.get("Relationship")
    property_names = request.form.getlist("property_name")
    property_values = request.form.getlist("property_value")
    print("property_names", property_names)
    print("property_values", property_values)
    global dict
    for name, value in zip(property_names, property_values):
        unidecode_text = unidecode(name).replace(" ", "").title()
        if name:
            if unidecode_text and unidecode_text not in dict.keys():
                dict[unidecode_text] = name
                print("dict[unidecode_text]", dict[unidecode_text])
            my_dict[unidecode_text] = value
    print("Node properties:", my_dict)
    try:
        with driver.session() as session:
            # session.run(them(my_dict))
            session.run(them(my_dict, relationship, parent_node))
            flash("Thêm kiến thức thành công!", "success")
    except Exception as e:
        flash(f"Thêm kiến thức thất bại! {e}", "error")
        print(f"Error: {e}")

    return redirect(url_for("index"))


@app.route("/delete-node", methods=["POST"])
def delete_node():
    title = request.form.get("Title")
    print(title)
    try:
        with driver.session() as session:
            session.run(xoa(title))
            flash("Xóa kiến thức thành công!", "success")
    except Exception as e:
        flash(f"Xóa kiến thức thất bại! {e}", "error")
        print(f"Error: {e}")

    return redirect(url_for("index"))


@app.route("/edit-node", methods=["POST"])
def edit_node():
    my_dict = {}
    form_data = request.form.to_dict()  # Convert form data to a dictionary
    print("form_data", form_data)
    # labels = request.form.get("labels")
    for key, value in request.form.items():
        if key not in ["property_name", "property_value"]:
            my_dict[key] = value

    property_names = request.form.getlist("property_name")
    property_values = request.form.getlist("property_value")

    for name, value in zip(property_names, property_values):
        if name:
            my_dict[name] = value
    try:
        with driver.session() as session:
            session.run(sua(my_dict["Title"], my_dict))
            flash("Sửa kiến thức thành công!", "success")
    except Exception as e:
        flash(f"Sửa kiến thức thất bại! {e}", "error")
        print(f"Error: {e}")

    return redirect(url_for("index"))


@app.route("/detail/<labels>")
def detail_node(labels):
    global dict
    before_list = []
    after_list = []
    relationship_list = []
    try:
        with driver.session() as session:
            before = session.run(
                create_query(labels, 0)
            )  # lấy ds tất cả node r liên quan phải có trước
            after = session.run(
                create_query(labels, 1)
            )  # lấy ds tất cả node r liên quan có sau
            for start in before:
                relationship_cmd = (
                    'MATCH ()-[r]->()\nwhere elementId(r)= "'
                    + start["r"].element_id
                    + '"\nRETURN type(r) as type'
                )
                relationship = session.run(relationship_cmd)
                type_r = relationship.data()[0]["type"]
                relationship_list.append(type_r)
                before_node = {
                    "labels": list(start["startNode"].labels)[0],
                    "title": start["startNode"]["Title"],
                }
                before_list.append(before_node)
            for end in after:
                after_node = {
                    "labels": list(end["endNode"].labels)[0],
                    "title": end["endNode"]["Title"],
                }
                after_list.append(after_node)
            command = 'MATCH (n) \nWHERE "' + labels + '"IN labels(n)\nRETURN n'
            result = session.run(command)

            for record in result:
                node = record["n"]
                # Convert the node to a dictionary
                node_data = {"labels": list(node.labels)[0], **node._properties}
                # print("node", node._properties)
            # global dict
    except Exception as e:
        print(f"Error: {e}")

    return render_template(
        "detail.html",
        dict=dict,
        relationship=relationship_list,
        before=before_list,
        after=after_list,
        node=node_data,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
