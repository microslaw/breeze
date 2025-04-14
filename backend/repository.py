import pandas as pd
import sqlite3
from backend.datatypes import NodeInstance
from backend.datatypes import NodeLink
from backend.datatypes import NodeType
import os
import shutil
import pickle


class ObjectNotInDBException(Exception):
    pass


class ObjectAlreadyInDBException(Exception):
    pass


class Repository:

    def __init__(self, db_name="db.sqlite3", db_folder_path="backend/data"):
        self.db_name = db_name
        self.db_folder_path = db_folder_path
        self.init_db()

    def write_object(
        self,
        object: object,
        producer_node_id: int,
        producer_node_output: str = None,
    ) -> None:
        if producer_node_output is None:
            object_name = f"{producer_node_id}-output"
        else:
            object_name = f"{producer_node_id}-{producer_node_output}-output"

        with open(f"{self.db_folder_path}/objects/{object_name}", "wb") as f:
            pickle.dump(object, f)

    def read_object(
        self,
        producer_node_id: int,
        producer_node_output: str = None,
    ) -> object:
        self.check_node_instance_exists(producer_node_id)

        if producer_node_output is None:
            object_name = f"{producer_node_id}-output"
        else:
            object_name = f"{producer_node_id}-{producer_node_output}-output"

        full_path = f"{self.db_folder_path}/objects/{object_name}"
        if not os.path.isfile(full_path):
            raise ObjectNotInDBException(
                f"Processing result of node with node_id={producer_node_id} not found"
            )

        with open(full_path, "rb") as f:
            return pickle.load(f)

    def get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(f"{self.db_folder_path}/{self.db_name}")

    def get_cursor(self) -> sqlite3.Cursor:
        return self.get_connection().cursor()

    def execute(self, query: str) -> None:
        cursor = self.get_cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(query)
        cursor.connection.commit()
        cursor.connection.close()

    def fetchall(self, query: str) -> list[tuple]:
        cursor = self.get_cursor()
        fetched = cursor.execute(query).fetchall()
        cursor.connection.commit()
        cursor.connection.close()
        return fetched

    def fetchone(self, query: str) -> tuple:
        cursor = self.get_cursor()
        fetched = cursor.execute(query).fetchone()
        cursor.connection.commit()
        cursor.connection.close()
        return fetched

    def from_csv(self, filename: str, table_name: str) -> None:
        df = pd.read_csv(filename)
        connection = self.get_connection()
        df.to_sql(table_name, connection, if_exists="append", index=False)
        connection.close()

    def init_db(self) -> None:
        if os.path.exists(self.db_folder_path):
            shutil.rmtree(self.db_folder_path)
        os.mkdir(self.db_folder_path)
        os.mkdir(f"{self.db_folder_path}/objects")

        self.execute("DROP TABLE IF EXISTS nodeLinks")
        self.execute(
            """CREATE TABLE nodeLinks (
                origin_node_id INTEGER NOT NULL,
                origin_node_output TEXT,
                destination_node_id INTEGER NOT NULL,
                destination_node_input TEXT,
                FOREIGN KEY (origin_node_id) REFERENCES nodeInstances(node_id),
                FOREIGN KEY (destination_node_id) REFERENCES nodeInstances(node_id)
                )"""
        )

        self.execute("DROP TABLE IF EXISTS nodeInstances")
        self.execute(
            """CREATE TABLE nodeInstances (
                node_id INTEGER PRIMARY KEY,
                node_type TEXT NOT NULL
                )"""
        )

    def get_all_node_instance_ids(self) -> list[int]:
        return [i[0] for i in self.fetchall("SELECT node_id FROM nodeInstances")]

    def check_node_instance_exists(self, node_id: int, raise_on=False) -> None:
        if (
            self.fetchone(
                f"SELECT node_id FROM nodeINstances WHERE node_id = {node_id}"
            )
            is None
        ):
            if raise_on == False:
                raise ObjectNotInDBException(
                    f"Node instance with node_id={node_id} not found"
                )
        else:
            if raise_on == True:
                raise ObjectAlreadyInDBException(
                    f"Node instance with node_id={node_id} already exists"
                )

    def get_node_instance(self, node_id: int) -> NodeInstance:
        self.check_node_instance_exists(node_id)
        nodeRow = self.fetchone(
            f"SELECT * FROM nodeInstances WHERE node_id = {node_id}"
        )
        return NodeInstance(nodeRow[0], nodeRow[1])

    def get_new_node_instance_id(self) -> int:
        new_id = self.fetchone("SELECT MAX(node_id) FROM nodeInstances")[0]
        if new_id is None:
            new_id = 0
        else:
            new_id += 1
        return new_id

    def create_node_instance(self, node_instance: NodeInstance) -> int:
        """
        Returns id of new node instance
        """
        node_id = self.get_new_node_instance_id()
        self.execute(
            f"INSERT INTO nodeInstances VALUES ({node_id}, '{node_instance.node_type}')"
        )
        return node_id

    def delete_node_instance(self, node_id: int) -> None:

        linksToDelete = self.get_links_by_origin_node_id(
            node_id
        ) + self.get_links_by_destination_node_id(node_id)
        for link in linksToDelete:
            self.delete_node_link(link)

        self.execute(f"DELETE FROM nodeInstances WHERE node_id = {node_id}")

    def get_links_by_origin_node_id(self, node_id: int) -> list[NodeLink]:
        self.check_node_instance_exists(node_id)
        linkRows = self.fetchall(
            f"SELECT * FROM nodeLinks WHERE origin_node_id = {node_id}"
        )
        return [
            NodeLink(linkRow[0], linkRow[1], linkRow[2], linkRow[3])
            for linkRow in linkRows
        ]

    def get_links_by_destination_node_id(self, node_id: int) -> list:
        self.check_node_instance_exists(node_id)
        linkRows = self.fetchall(
            f"SELECT * FROM nodeLinks WHERE destination_node_id = {node_id}"
        )
        return [
            NodeLink(linkRow[0], linkRow[1], linkRow[2], linkRow[3])
            for linkRow in linkRows
        ]

    def get_all_links(self) -> list:
        linkRows = self.fetchall(f"SELECT * FROM nodeLinks")
        return [
            NodeLink(linkRow[0], linkRow[1], linkRow[2], linkRow[3])
            for linkRow in linkRows
        ]

    def get_links_by_destination_node_id(self, node_id: int) -> list[NodeLink]:
        self.check_node_instance_exists(node_id)
        linkRows = self.fetchall(
            f"SELECT * FROM nodeLinks WHERE destination_node_id = {node_id}"
        )
        return [
            NodeLink(linkRow[0], linkRow[1], linkRow[2], linkRow[3])
            for linkRow in linkRows
        ]

    def get_all_links(self) -> list[NodeLink]:
        linkRows = self.fetchall(f"SELECT * FROM nodeLinks")
        return [
            NodeLink(linkRow[0], linkRow[1], linkRow[2], linkRow[3])
            for linkRow in linkRows
        ]

    def check_node_link_exists(self, link: NodeLink, raise_on: bool = False) -> None:
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

        if self.fetchone(select_one_query) is None:
            if raise_on == False:
                raise ObjectNotInDBException(f"Node link {link.toJSON()} not found")
        else:
            if raise_on == True:
                raise ObjectAlreadyInDBException(
                    f"Node link {link.toJSON()} already exists"
                )

    def create_node_link(self, link: NodeLink) -> None:
        self.check_node_link_exists(link, raise_on=True)
        self.check_node_instance_exists(link.origin_node_id)
        self.check_node_instance_exists(link.destination_node_id)

        origin_node_output = (
            link.origin_node_output if link.origin_node_output is not None else "NULL"
        )
        query = f"""
            INSERT INTO nodeLinks
                VALUES ({link.origin_node_id}, {origin_node_output}, {link.destination_node_id}, '{link.destination_node_input}')
        """
        self.execute(query)

    def delete_node_link(self, link: NodeLink) -> None:
        """
        Each link is unique only when all fields are the same, so all fields are used
        """
        self.check_node_link_exists(link)
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
        self.execute(query)

    def check_node_type_exists(self, node_type: int, raise_on: bool = False) -> None:
        if node_type not in self.get_all_node_types():
            if raise_on == False:
                raise ObjectNotInDBException(f"Node type {node_type} not found")
        else:
            if raise_on == True:
                raise ObjectAlreadyInDBException(
                    f"Node type {node_type} already exists"
                )

    def get_all_node_types(self) -> list:
        return [node_type.get_name() for node_type in NodeType.all_udn]

    def get_node_type(self, node_type_name: str) -> NodeType:
        self.check_node_type_exists(node_type_name)
        for node_type in NodeType.all_udn:
            if node_type.get_name() == node_type_name:
                return node_type

    def get_prerequisite_node_ids(self, node_id: int) -> list[int]:
        self.check_node_instance_exists(node_id)

        node_rows = self.fetchall(
            f"""SELECT node_id
            FROM nodeInstances
            JOIN nodeLinks ON origin_node_id = node_id
            WHERE destination_node_id = {node_id}"""
        )

        return [node_row[0] for node_row in node_rows]
