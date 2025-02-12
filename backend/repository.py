import pickle
import sqlite3
from NodeInstance import NodeInstance
from NodeLink import NodeLink


def write_pickle(object, path):
    with open(path, "wb") as f:
        pickle.dump(object, f)


def read_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def execute(query):
    cursor = sqlite3.connect("db.sqlite3").cursor()
    cursor.execute(query)
    cursor.connection.commit()


def fetchall(query):
    cursor = sqlite3.connect("db.sqlite3").cursor()
    fetched = cursor.execute(query).fetchall()
    return fetched


def fetchone(query):
    cursor = sqlite3.connect("db.sqlite3").cursor()
    fetched = cursor.execute(query).fetchone()
    return fetched


def init_db():
    execute("DROP TABLE IF EXISTS nodeInstances")
    execute(
        """CREATE TABLE nodeInstances (
            node_id INTEGER PRIMARY KEY,
            node_type TEXT NOT NULL
            )"""
    )

    execute("DROP TABLE IF EXISTS nodeLinks")
    execute(
        """CREATE TABLE nodeLinks (
            origin_node_id INTEGER NOT NULL,
            origin_node_output TEXT NOT NULL,
            destination_node_id INTEGER NOT NULL,
            destination_node_input TEXT,
            FOREIGN KEY (origin_node_id) REFERENCES nodeInstances(node_id),
            FOREIGN KEY (destination_node_id) REFERENCES nodeInstances(node_id)
            )"""
    )


def get_all_node_instance_ids():
    return [i[0] for i in fetchall("SELECT node_id FROM nodeInstances")]


def get_node_instance(node_id) -> NodeInstance:
    nodeRow = fetchone(f"SELECT * FROM nodeInstances WHERE node_id = {node_id}")
    return NodeInstance(nodeRow[0], nodeRow[1])


def create_node_instance(node_instance: NodeInstance):
    execute(
        f"INSERT INTO nodeInstances VALUES ({node_instance.node_id}, '{node_instance.node_type}')"
    )


def delete_node_instance(node_id):
    execute(f"DELETE FROM nodeInstances WHERE node_id = {node_id}")

    linksToDelete = get_links_by_origin_node_id(node_id) + get_links_by_destination_node_id(node_id)
    for link in linksToDelete:
        delete_node_link(link)


def get_links_by_origin_node_id(node_id):
    linkRows = fetchall(f"SELECT * FROM nodeLinks WHERE origin_node_id = {node_id}")
    return [
        NodeLink(linkRow[0], linkRow[1], linkRow[2], linkRow[3]) for linkRow in linkRows
    ]


def get_links_by_destination_node_id(node_id):
    linkRows = fetchall(
        f"SELECT * FROM nodeLinks WHERE destination_node_id = {node_id}"
    )
    return [
        NodeLink(linkRow[0], linkRow[1], linkRow[2], linkRow[3]) for linkRow in linkRows
    ]


def create_node_link(link: NodeLink):
    execute(
        f"INSERT INTO nodeLinks VALUES ({link.origin_node_id}, '{link.origin_node_output}', {link.destination_node_id}, '{link.destination_node_input}')"
    )


def delete_node_link(link: NodeLink):
    """
    Each link is unique only when all fields are the same, so all fields are used
    """
    execute(
        f"""
        DELETE FROM nodeLinks
            WHERE origin_node_id = {link.origin_node_id}
            AND origin_node_output = '{link.origin_node_output}'
            AND destination_node_id = {link.destination_node_id}
            AND destination_node_input = '{link.destination_node_input}'
        """
    )
