import pandas as pd
import sqlite3
from backend.datatypes import NodeInstance
from backend.datatypes import NodeLink
from backend.datatypes import NodeType


class ObjectNotInDBException(Exception):
    pass

class ObjectAlreadyInDBException(Exception):
    pass


def execute(query: str) -> None:
    cursor = sqlite3.connect("db.sqlite3").cursor()
    cursor.execute(query)
    cursor.connection.commit()


def fetchall(query: str) -> list:
    cursor = sqlite3.connect("db.sqlite3").cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    fetched = cursor.execute(query).fetchall()
    return fetched


def fetchone(query: str) -> tuple:
    cursor = sqlite3.connect("db.sqlite3").cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    fetched = cursor.execute(query).fetchone()
    return fetched


def from_csv(filename: str, table_name: str):
    con = sqlite3.connect("db.sqlite3")

    df = pd.read_csv(filename)
    df.to_sql(table_name, con, if_exists="append", index=False)

    con.close()


def init_db() -> None:
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
            origin_node_output TEXT,
            destination_node_id INTEGER NOT NULL,
            destination_node_input TEXT,
            FOREIGN KEY (origin_node_id) REFERENCES nodeInstances(node_id),
            FOREIGN KEY (destination_node_id) REFERENCES nodeInstances(node_id)
            )"""
    )


def get_all_node_instance_ids() -> list:
    return [i[0] for i in fetchall("SELECT node_id FROM nodeInstances")]


def assert_node_instance_exists(node_id, raise_on=False) -> None:
    if fetchone(f"SELECT node_id FROM nodeINstances WHERE node_id = {node_id}") is None:
        if raise_on==False:
            raise ObjectNotInDBException(f"Node instance with node_id={node_id} not found")
    else:
        if raise_on==True:
            raise ObjectAlreadyInDBException(f"Node instance with node_id={node_id} already exists")


def get_node_instance(node_id) -> NodeInstance:
    assert_node_instance_exists(node_id)
    nodeRow = fetchone(f"SELECT * FROM nodeInstances WHERE node_id = {node_id}")
    return NodeInstance(nodeRow[0], nodeRow[1])


def get_new_node_instance_id():
    new_id = fetchone("SELECT MAX(node_id) FROM nodeInstances")[0]
    if new_id is None:
        new_id = 0
    else:
        new_id += 1
    return new_id


def create_node_instance(node_instance: NodeInstance) -> int:
    """
    Returns id of new node instance
    """
    node_id = get_new_node_instance_id()
    execute(
        f"INSERT INTO nodeInstances VALUES ({node_id}, '{node_instance.node_type}')"
    )
    return node_id


def delete_node_instance(node_id: int) -> None:

    linksToDelete = get_links_by_origin_node_id(
        node_id
    ) + get_links_by_destination_node_id(node_id)
    for link in linksToDelete:
        delete_node_link(link)

    execute(f"DELETE FROM nodeInstances WHERE node_id = {node_id}")


def get_links_by_origin_node_id(node_id: int) -> list:
    assert_node_instance_exists(node_id)
    linkRows = fetchall(f"SELECT * FROM nodeLinks WHERE origin_node_id = {node_id}")
    return [
        NodeLink(linkRow[0], linkRow[1], linkRow[2], linkRow[3]) for linkRow in linkRows
    ]


def assert_node_link_exists(link: NodeLink, raise_on=False) -> None:
    select_one_query = f"""
        SELECT * FROM nodeLinks
            WHERE origin_node_id = {link.origin_node_id}
            AND destination_node_id = {link.destination_node_id}
            AND destination_node_input = '{link.destination_node_input}'
        """
    if link.origin_node_output is not None:
        select_one_query += f" AND origin_node_output = '{link.origin_node_output}'"
    else:
        select_one_query += f" AND origin_node_output IS NULL"

    if fetchone(select_one_query) is None:
        if raise_on == False:
            raise ObjectNotInDBException(f"Node link {link.toJSON()} not found")
    else:
        if raise_on == True:
            raise ObjectAlreadyInDBException(f"Node link {link.toJSON()} already exists")


def get_links_by_destination_node_id(node_id: int) -> list:
    assert_node_instance_exists(node_id)
    linkRows = fetchall(
        f"SELECT * FROM nodeLinks WHERE destination_node_id = {node_id}"
    )
    return [
        NodeLink(linkRow[0], linkRow[1], linkRow[2], linkRow[3]) for linkRow in linkRows
    ]


def create_node_link(link: NodeLink) -> None:
    assert_node_link_exists(link, raise_on=True)

    origin_node_output = (
        link.origin_node_output if link.origin_node_output is not None else "NULL"
    )
    query = f"""
        INSERT INTO nodeLinks
            VALUES ({link.origin_node_id}, {origin_node_output}, {link.destination_node_id}, '{link.destination_node_input}')
    """
    execute(query)


def delete_node_link(link: NodeLink) -> None:
    """
    Each link is unique only when all fields are the same, so all fields are used
    """
    assert_node_link_exists(link)
    query = f"""
        DELETE FROM nodeLinks
            WHERE origin_node_id = {link.origin_node_id}
            AND destination_node_id = {link.destination_node_id}
            AND destination_node_input = '{link.destination_node_input}'
        """

    if link.origin_node_output is not None:
        query += f" AND origin_node_output = '{link.origin_node_output}'"
    else:
        query += f" AND origin_node_output IS NULL"
    execute(query)


def assert_node_type_exists(node_type: int, raise_on = False) -> None:
    if node_type not in get_all_node_types():
        if raise_on == False:
            raise ObjectNotInDBException(f"Node type {node_type} not found")
    else:
        if raise_on == True:
            raise ObjectAlreadyInDBException(f"Node type {node_type} already exists")

def get_all_node_types() -> list:
    return [node_type.get_name() for node_type in NodeType.all_udn]


def get_node_type(node_type_name: str) -> NodeType:
    assert_node_type_exists(node_type_name)
    for node_type in NodeType.all_udn:
        if node_type.get_name() == node_type_name:
            return node_type
