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

    def get_output_path(self, node_id: int, output_name: str):
        if output_name is None:
            object_name = f"{node_id}-output"
        else:
            object_name = f"{node_id}-{output_name}-output"
        return f"{self.db_folder_path}/objects/{object_name}"

    def write_output(
        self,
        object: object,
        producer_node_id: int,
        producer_node_output: str = None,
    ) -> None:

        with open(
            self.get_output_path(producer_node_id, producer_node_output), "wb"
        ) as f:
            pickle.dump(object, f)

    def does_output_exist(self, node_id: int, output_name: str = None) -> bool:
        return os.path.isfile(self.get_output_path(node_id, output_name))

    def read_output(
        self,
        producer_node_id: int,
        producer_node_output: str = None,
    ) -> object:
        self.check_node_instance_exists(producer_node_id)

        if not self.does_output_exist(producer_node_id, producer_node_output):
            raise ObjectNotInDBException(
                f"Processing result of node with node_id={producer_node_id} not found"
            )

        with open(
            self.get_output_path(producer_node_id, producer_node_output), "rb"
        ) as f:
            return pickle.load(f)

    def get_kwarg_path(self, node_id, kwarg_name):
        return f"{self.db_folder_path}/objects/{node_id}-{kwarg_name}-kwarg"

    def does_kwarg_exist(self, node_id: int, kwarg_name: str) -> bool:
        return os.path.isfile(self.get_kwarg_path(node_id, kwarg_name))

    def write_kwarg(
        self,
        object: object,
        parent_node_id: int,
        kwarg_name: str = None,
    ) -> None:
        node_type_name = self.get_node_instance(parent_node_id).node_type
        self.check_node_kwarg_exists(node_type_name, kwarg_name)

        with open(self.get_kwarg_path(parent_node_id, kwarg_name), "wb") as f:
            pickle.dump(object, f)

    def read_kwarg(
        self,
        parent_node_id: int,
        kwarg_name: str = None,
    ) -> object:
        node_type_name = self.get_node_instance_type_name(parent_node_id)
        self.check_node_kwarg_exists(node_type_name, kwarg_name)

        full_path = f"{self.db_folder_path}/objects/{parent_node_id}-{kwarg_name}-kwarg"
        if not self.does_kwarg_exist(parent_node_id, kwarg_name):
            raise ObjectNotInDBException(
                f"Kwarg {kwarg_name} of node with node_id={parent_node_id} not found"
            )

        with open(full_path, "rb") as f:
            return pickle.load(f)

    def read_instance_kwargs(self, instance_id: int):
        self.check_node_instance_exists(instance_id)

        object_paths = os.listdir(f"{self.db_folder_path}/objects")
        # e.g. object_path: 3-colname-kwarg
        # object_path.split("-")[0] == 3 <instance_id> and object_path.split("-")[1] == colname <kwarg_name>

        instance_kwarg_names = [
            filename.split("-")[1]
            for filename in object_paths
            if int(filename.split("-")[0]) == instance_id
        ]

        return {
            name: self.read_kwarg(instance_id, name) for name in instance_kwarg_names
        }

    def load_workflow(self, path, filetype="csv"):
        if filetype == "csv":
            self.from_csv(f"{path}/nodeInstances.csv", "nodeInstances")
            self.from_csv(f"{path}/nodeLinks.csv", "nodeLinks")
        else:
            raise NotImplementedError

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

    def fetchall(self, query: str, named=False) -> list[tuple]:
        cursor = self.get_cursor()
        fetched = cursor.execute(query).fetchall()
        cursor.connection.commit()
        cursor.connection.close()

        if named:
            colnames = [desc[0] for desc in cursor.description]
            fetched = [
                {name: val for name, val in zip(colnames, fetched_row)}
                for fetched_row in fetched
            ]
        return fetched

    def fetchone(self, query: str, named=False) -> tuple:
        cursor = self.get_cursor()
        fetched = cursor.execute(query).fetchone()
        cursor.connection.commit()
        cursor.connection.close()

        if named:
            colnames = [desc[0] for desc in cursor.description]
            fetched = {name: val for name, val in zip(colnames, fetched)}

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
                node_link_id INTEGER NOT NULL,
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
                node_type TEXT NOT NULL,
                position_x INTEGER NOT NULL,
                position_y INTEGER NOT NULL,
                instance_name TEXT
                )"""
        )

    def get_all_node_instances(self) -> list[NodeInstance]:
        rows = self.fetchall("SELECT * FROM nodeInstances", named=True)
        return [NodeInstance.fromNameDict(row) for row in rows]

    def check_node_instance_exists(self, node_id: int, raise_on=False) -> None:
        if (
            self.fetchone(
                f"SELECT node_id FROM nodeInstances WHERE node_id = {node_id}"
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
        node_row = self.fetchone(
            f"SELECT * FROM nodeInstances WHERE node_id = {node_id}", named=True
        )
        instance = NodeInstance.fromNameDict(node_row)
        instance.overwrite_kwargs = self.read_instance_kwargs(instance.node_id)
        return instance

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

        nulled_instance_name = (
            f"'{node_instance.instance_name}'"
            if node_instance.instance_name is not None
            else "NULL"
        )
        self.execute(
            f"""INSERT INTO nodeInstances VALUES (
                {node_id},
                '{node_instance.node_type}',
                {node_instance.position_x},
                {node_instance.position_y},
                {nulled_instance_name})"""
        )
        return node_id

    def delete_node_instance(self, node_id: int) -> None:

        linksToDelete = self.get_links_by_origin_node_id(
            node_id
        ) + self.get_links_by_destination_node_id(node_id)
        for link in linksToDelete:
            self.delete_node_link(link.node_link_id)

        self.execute(f"DELETE FROM nodeInstances WHERE node_id = {node_id}")

    def get_links_by_origin_node_id(self, node_id: int) -> list[NodeLink]:
        self.check_node_instance_exists(node_id)
        linkRows = self.fetchall(
            f"SELECT * FROM nodeLinks WHERE origin_node_id = {node_id}", named=True
        )
        return [NodeLink.fromNameDict(linkRow) for linkRow in linkRows]

    def get_links_by_destination_node_id(self, node_id: int) -> list[NodeLink]:
        self.check_node_instance_exists(node_id)
        linkRows = self.fetchall(
            f"SELECT * FROM nodeLinks WHERE destination_node_id = {node_id}", named=True
        )
        return [NodeLink.fromNameDict(linkRow) for linkRow in linkRows]

    def get_all_links(
        self, origin_node_id=None, destination_node_id=None
    ) -> list[NodeLink]:
        # TODO: Simplify this query
        query = f"SELECT * FROM nodeLinks "
        if origin_node_id is not None:
            query += f"WHERE origin_node_id = {origin_node_id} "
        if destination_node_id is not None:
            if origin_node_id is not None:
                query += "AND "
            else:
                query += "WHERE "
            query += f"destination_node_id = {destination_node_id} "

        linkRows = self.fetchall(query, named=True)
        return [NodeLink.fromNameDict(linkRow) for linkRow in linkRows]

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
                raise ObjectNotInDBException(f"Node link {link.toNameDict()} not found")
        else:
            if raise_on == True:
                raise ObjectAlreadyInDBException(
                    f"Node link {link.toNameDict()} already exists"
                )

    def check_node_link_exists_by_id(
        self, node_link_id, raise_on: bool = False
    ) -> None:
        query = f"""
            SELECT * FROM nodeLinks
                WHERE node_link_id = {node_link_id}
            """
        if self.fetchone(query) is None:
            if raise_on == False:
                raise ObjectNotInDBException(
                    f"Node link with node_link_id={node_link_id} not found"
                )
        else:
            if raise_on == True:
                raise ObjectAlreadyInDBException(
                    f"Node link with node_link_id={node_link_id} already exists"
                )

    def get_node_link(self, node_link_id: int) -> NodeLink:
        self.check_node_link_exists_by_id(node_link_id)
        node_row = self.fetchone(
            f"SELECT * FROM nodeLinks WHERE node_link_id = {node_link_id}", named=True
        )
        instance = NodeLink.fromNameDict(node_row)
        return instance

    def get_new_node_link_id(self) -> int:
        new_id = self.fetchone("SELECT MAX(node_link_id) FROM nodeLinks")[0]
        if new_id is None:
            new_id = 0
        else:
            new_id += 1
        return new_id

    def create_node_link(self, link: NodeLink) -> None:
        self.check_node_link_exists(link, raise_on=True)
        self.check_node_instance_exists(link.origin_node_id)
        self.check_node_instance_exists(link.destination_node_id)

        node_link_id = self.get_new_node_link_id()

        origin_node_output = (
            link.origin_node_output if link.origin_node_output is not None else "NULL"
        )
        query = f"""
            INSERT INTO nodeLinks
                VALUES ({node_link_id}, {link.origin_node_id}, {origin_node_output}, {link.destination_node_id}, '{link.destination_node_input}')
        """
        self.execute(query)
        return node_link_id

    def delete_node_link(self, node_link_id: int) -> None:
        """
        Each link is unique only when all fields are the same, so all fields are used
        """
        self.check_node_link_exists_by_id(node_link_id)
        query = f"""
            DELETE FROM nodeLinks
                WHERE node_link_id = {node_link_id}
            """

        self.execute(query)

    def check_node_type_exists(
        self, node_type_name: str, raise_on: bool = False
    ) -> None:
        if node_type_name not in self.get_all_node_types():
            if raise_on == False:
                raise ObjectNotInDBException(f"Node type {node_type_name} not found")
        else:
            if raise_on == True:
                raise ObjectAlreadyInDBException(
                    f"Node type {node_type_name} already exists"
                )

    def check_node_kwarg_exists(self, node_type_name: str, kwarg_name: str):

        node_type = self.get_node_type(node_type_name)
        if kwarg_name not in node_type.get_arg_names():
            raise ObjectNotInDBException(
                f"""Nodes of type_name= "{node_type.get_name()}" do not have any argument with kwarg_name="{kwarg_name}\""""
            )

    def get_all_node_types(self) -> list[NodeType]:
        return [node_type.get_name() for node_type in NodeType.all_udn]

    def get_node_instance_type_name(self, node_id: int) -> str:
        self.check_node_instance_exists(node_id)
        node_type_name = self.fetchone(
            f"SELECT node_type FROM nodeInstances WHERE node_id = {node_id}"
        )[0]
        return node_type_name

    def get_node_type(self, node_type_name: str) -> NodeType:
        self.check_node_type_exists(node_type_name)
        for node_type in NodeType.all_udn:
            if node_type.get_name() == node_type_name:
                return node_type

    def get_arg_type(self, node_type_name: str, arg_name: str):
        self.check_node_kwarg_exists(node_type_name, arg_name)
        return self.get_node_type(node_type_name).get_arg_types().get(arg_name)

    def get_prerequisite_node_ids(self, node_id: int) -> list[int]:
        self.check_node_instance_exists(node_id)

        node_rows = self.fetchall(
            f"""SELECT node_id
            FROM nodeInstances
            JOIN nodeLinks ON origin_node_id = node_id
            WHERE destination_node_id = {node_id}""",
            named=True,
        )

        return [node_row["node_id"] for node_row in node_rows]
