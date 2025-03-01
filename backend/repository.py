import sqlite3
from backend.datatypes import NodeInstance
from backend.datatypes import NodeLink
from backend.datatypes import NodeType


class ObjectNotInDBException(Exception):
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
            origin_node_output TEXT NOT NULL,
            destination_node_id INTEGER NOT NULL,
            destination_node_input TEXT,
            FOREIGN KEY (origin_node_id) REFERENCES nodeInstances(node_id),
            FOREIGN KEY (destination_node_id) REFERENCES nodeInstances(node_id)
            )"""
    )


def get_all_node_instance_ids() -> list:
    return [i[0] for i in fetchall("SELECT node_id FROM nodeInstances")]


def assert_node_instance_exists(node_id) -> None:
    if fetchone(f"SELECT node_id FROM nodeINstances WHERE node_id = {node_id}") is None:
        raise ObjectNotInDBException(f"Node instance with node_id={node_id} not found")


def get_node_instance(node_id) -> NodeInstance:
    assert_node_instance_exists(node_id)
    nodeRow = fetchone(f"SELECT * FROM nodeInstances WHERE node_id = {node_id}")
    return NodeInstance(nodeRow[0], nodeRow[1])


def create_node_instance(node_instance: NodeInstance) -> None:
    execute(
        f"INSERT INTO nodeInstances VALUES ({node_instance.node_id}, '{node_instance.node_type}')"
    )


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


def assert_node_link_exists(link: NodeLink) -> None:
    select_one_query = f"""
        SELECT * FROM nodeLinks
            WHERE origin_node_id = {link.origin_node_id}
            AND origin_node_output = '{link.origin_node_output}'
            AND destination_node_id = {link.destination_node_id}
            AND destination_node_input = '{link.destination_node_input}'
        """
    if fetchone(select_one_query) is None:
        raise ObjectNotInDBException(f"Node link {link.toJSON()} not found")


def get_links_by_destination_node_id(node_id: int) -> list:
    assert_node_instance_exists(node_id)
    linkRows = fetchall(
        f"SELECT * FROM nodeLinks WHERE destination_node_id = {node_id}"
    )
    return [
        NodeLink(linkRow[0], linkRow[1], linkRow[2], linkRow[3]) for linkRow in linkRows
    ]


def create_node_link(link: NodeLink) -> None:
    execute(
        f"INSERT INTO nodeLinks VALUES ({link.origin_node_id}, '{link.origin_node_output}', {link.destination_node_id}, '{link.destination_node_input}')"
    )


def delete_node_link(link: NodeLink) -> None:
    """
    Each link is unique only when all fields are the same, so all fields are used
    """
    assert_node_link_exists(link)
    execute(
        f"""
        DELETE FROM nodeLinks
            WHERE origin_node_id = {link.origin_node_id}
            AND origin_node_output = '{link.origin_node_output}'
            AND destination_node_id = {link.destination_node_id}
            AND destination_node_input = '{link.destination_node_input}'
        """
    )


def assert_node_type_exists(node_type: int) -> None:
    if node_type not in get_all_node_types():
        raise ObjectNotInDBException(f"Node type {node_type} not found")


def get_all_node_types() -> list:
    return [node_type.get_name() for node_type in NodeType.all_udn]


def get_node_type(node_type_name: str) -> NodeType:
    assert_node_type_exists(node_type_name)
    for node_type in NodeType.all_udn:
        if node_type.get_name() == node_type_name:
            return node_type
