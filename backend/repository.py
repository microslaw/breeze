import pandas as pd
import sqlite3
from backend.datatypes import NodeInstance
from backend.datatypes import NodeLink
from backend.datatypes import NodeType
import os
import shutil
import pickle
from datetime import datetime
from typing import Optional, Any


class ObjectNotInDBException(Exception):
    pass


class ObjectAlreadyInDBException(Exception):
    pass


KWARG_FILE_ENDING = "kwarg"
OUTPUT_FILE_ENDING = "output"


class Repository:
    """
    Handles persistance and reading of basic datatypes as well as outputs and arguments
    """

    def __init__(
        self, db_name: str = "db.sqlite3", db_folder_path: str = "backend/data"
    ):
        self.db_name = db_name
        self.db_folder_path = db_folder_path
        self.init_db()

    def get_output_path(self, node_id: int, output_name: Optional[str]):
        """
        Pieces together path to a specific output
        """
        if output_name is None:
            object_name = f"{node_id}--{OUTPUT_FILE_ENDING}"
        else:
            object_name = f"{node_id}-{output_name}-{OUTPUT_FILE_ENDING}"
        return f"{self.db_folder_path}/objects/{object_name}"

    def write_output(
        self,
        object: object,
        producer_node_id: int,
        producer_node_output: Optional[str] = None,
    ) -> None:
        """
        Writes output of a specific node to a file
        """
        with open(
            self.get_output_path(producer_node_id, producer_node_output), "wb"
        ) as f:
            pickle.dump(object, f)

    def is_output_created(
        self, node_id: int, output_name: Optional[str] = None
    ) -> bool:
        return os.path.isfile(self.get_output_path(node_id, output_name))

    def delete_output(
        self,
        producer_node_id: int,
        producer_node_output: Optional[str] = None,
    ) -> None:
        """
        Removes file with specific output of a specific node
        """
        if self.is_output_created(producer_node_id, producer_node_output):
            os.remove(self.get_output_path(producer_node_id, producer_node_output))
        else:
            raise ObjectNotInDBException(
                f"Output {producer_node_output} of node {producer_node_id} does not exist"
            )

    def delete_all_outputs(self):
        for node_id in self.get_all_node_ids():
            if self.is_output_created(node_id):
                self.delete_output(node_id)

    def read_output(
        self,
        producer_node_id: int,
        producer_node_output: Optional[str] = None,
    ) -> object:
        """
        Reads output of a specific node from respective file
        """
        self.check_node_instance_exists(producer_node_id)

        if not self.is_output_created(producer_node_id, producer_node_output):
            raise ObjectNotInDBException(
                f"Processing result of node with node_id={producer_node_id} not found"
            )

        with open(
            self.get_output_path(producer_node_id, producer_node_output), "rb"
        ) as f:
            return pickle.load(f)

    def get_output_created_date(self, node_id: int) -> str:
        """
        Returns the node processing date. Relies on the time on which the
        output file was saved, therefore entrusting the timestamp to os
        """
        self.check_node_instance_exists(node_id)
        output_path = self.get_output_path(node_id, None)
        float_date = os.path.getmtime(output_path)
        return datetime.fromtimestamp(float_date)

    def get_kwarg_path(self, node_id: int, kwarg_name: str):
        """
        Pieces together path to a specific kwarg,
        """

        return (
            f"{self.db_folder_path}/objects/{node_id}-{kwarg_name}-{KWARG_FILE_ENDING}"
        )

    def is_kwarg_created(self, node_id: int, kwarg_name: str) -> bool:
        return os.path.isfile(self.get_kwarg_path(node_id, kwarg_name))

    def write_kwarg(
        self,
        object: object,
        parent_node_id: int,
        kwarg_name: str,
    ) -> None:
        """
        Writes a specific overwrite kwarg to a file
        """
        node_type_name = self.get_node_instance(parent_node_id).node_type_name
        self.does_node_have_kwarg(node_type_name, kwarg_name)
        self.delete_all_following_node_outputs(parent_node_id)

        with open(self.get_kwarg_path(parent_node_id, kwarg_name), "wb") as f:
            pickle.dump(object, f)

    def read_kwarg(
        self,
        parent_node_id: int,
        kwarg_name: str,
    ) -> object:
        """
        Reads a specific overwrite kwarg from a file
        """
        node_type_name = self.get_node_instance_type_name(parent_node_id)
        self.does_node_have_kwarg(node_type_name, kwarg_name)

        full_path = f"{self.db_folder_path}/objects/{parent_node_id}-{kwarg_name}-{KWARG_FILE_ENDING}"
        if not self.is_kwarg_created(parent_node_id, kwarg_name):
            raise ObjectNotInDBException(
                f"Kwarg {kwarg_name} of node with node_id={parent_node_id} not found"
            )

        with open(full_path, "rb") as f:
            return pickle.load(f)

    def read_instance_kwargs(self, instance_id: int):
        """
        Reads all overwrite kwargs of a specific node instance
        """
        self.check_node_instance_exists(instance_id)

        filenames = os.listdir(f"{self.db_folder_path}/objects")
        # e.g. object_path: 3-colname-kwarg
        # object_path.split("-")[0] == 3 <instance_id> and object_path.split("-")[1] == colname <kwarg_name>

        file_tuples = [filename.split("-") for filename in filenames]
        instance_kwarg_names = [
            argname
            for this_node_id, argname, type in file_tuples
            if int(this_node_id) == instance_id and type == KWARG_FILE_ENDING
        ]

        return {
            name: self.read_kwarg(instance_id, name) for name in instance_kwarg_names
        }

    def load_workflow(self, path: str, filetype: str = "csv"):
        """
        Loads a workflow (essentially a set of node instances and node links) from
        a file. Intended mostly for testing and tutorials, not for real user-made workflows
        """
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
        """
        Executes sql querry on linked database
        """
        cursor = self.get_cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(query)
        cursor.connection.commit()
        cursor.connection.close()

    def fetchall(self, query: str) -> list[str]:
        """
        Executes sql querry on a linked database and returns list of results
        as tuples
        """
        cursor = self.get_cursor()
        fetched = cursor.execute(query).fetchall()
        cursor.connection.commit()
        cursor.connection.close()

        return fetched

    def fetchall_named(self, query: str) -> list[dict[str, object]]:
        """
        Executes sql querry on a linked database and returns list of results,
        where each result is a dictionary in form of {colname:value}
        """
        cursor = self.get_cursor()
        fetched = cursor.execute(query).fetchall()
        cursor.connection.commit()
        cursor.connection.close()

        colnames = [desc[0] for desc in cursor.description]
        fetched = [
            {name: val for name, val in zip(colnames, fetched_row)}
            for fetched_row in fetched
        ]
        return fetched

    def fetchone(self, query: str) -> Any:
        """
        Executes sql querry on a linked database and returns singular result
        as tuple of values
        """
        cursor = self.get_cursor()
        fetched = cursor.execute(query).fetchone()
        cursor.connection.commit()
        cursor.connection.close()

        return fetched

    def fetchone_named(self, query: str) -> dict[str, Any]:
        """
        Executes sql querry on a linked database and returns singular result
        as dictionary has a form {colname:value}"""
        cursor = self.get_cursor()
        fetched = cursor.execute(query).fetchone()
        cursor.connection.commit()
        cursor.connection.close()

        colnames = [desc[0] for desc in cursor.description]
        fetched = {name: val for name, val in zip(colnames, fetched)}

        return fetched

    def from_csv(self, filename: str, table_name: str) -> None:
        """
        Appends contents of a csv to a table. Intended mostly for testing and tutorials
        """
        df: pd.DataFrame = pd.read_csv(filename)
        connection = self.get_connection()
        df.to_sql(table_name, connection, if_exists="append", index=False)
        connection.close()

    def init_db(self) -> None:
        """
        Creates a clean database. Will purge previous database
        """
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
        """
        Returns list of all node instances
        """
        rows = self.fetchall_named("SELECT * FROM nodeInstances")

        node_instances: list[NodeInstance] = []
        for row in rows:
            node_instance = NodeInstance.fromNameDict(row)
            node_instance.overwrite_kwargs = self.read_instance_kwargs(
                node_instance.node_id
            )
            node_instances.append(node_instance)
        return node_instances

    def get_all_node_ids(self) -> list[int]:
        """
        Returns a list of all node ids
        """
        rows = self.fetchall_named("SELECT node_id FROM nodeInstances")
        return [row["node_id"] for row in rows]

    def get_all_final_node_ids(self):
        """
        Returns ids of nodes that do not have any other nodes dependant on them (no links originating in them)
        """
        wrapped_node_ids = self.fetchall(
            "SELECT node_id FROM nodeInstances WHERE node_id NOT IN (SELECT origin_node_id FROM nodeLinks)"
        )

        return [node_id_tuple[0] for node_id_tuple in wrapped_node_ids]

    def check_node_instance_exists(self, node_id: int, raise_on: bool = False) -> None:
        """
        If raise_on == False, will raise if node does not exist
        If raise_on == True, will raise if node does exist
        Otherwise will not do anything
        """

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
        """
        Returns NodeInstance with specified node_id
        """
        self.check_node_instance_exists(node_id)
        node_row = self.fetchone_named(
            f"SELECT * FROM nodeInstances WHERE node_id = {node_id}"
        )
        instance = NodeInstance.fromNameDict(node_row)
        instance.overwrite_kwargs = self.read_instance_kwargs(instance.node_id)
        return instance

    def get_new_node_instance_id(self) -> int:
        """
        Generates node_id of next NodeInstance to be added.
        By default it is MAX(node_id)+1
        """
        new_id = self.fetchone("SELECT MAX(node_id) FROM nodeInstances")[0]
        if new_id is None:
            new_id = 0
        else:
            new_id += 1
        return new_id

    def create_node_instance(self, node_instance: NodeInstance) -> int:
        """
        Persists nodeInstance.
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
                '{node_instance.node_type_name}',
                {node_instance.position_x},
                {node_instance.position_y},
                {nulled_instance_name})"""
        )
        return node_id

    def update_node_instance(self, instance: NodeInstance, to_update_id: int) -> None:
        """
        Overwrites variables of already persisted NodeInstance identified by
        to_update_id, with values from to_update_id
        """
        self.check_node_instance_exists(to_update_id)

        sql_col_eq_values = ", ".join(
            [
                f"{colname}='{value}'"
                for colname, value in instance.toNameDict().items()
                if value is not None and colname != "overwrite_kwargs"
            ]
        )

        query = f"""
        UPDATE nodeInstances
        SET {sql_col_eq_values}
        WHERE node_id = {to_update_id}
        """
        self.execute(query)

    def delete_node_instance(self, node_id: int) -> None:
        """
        Removes node instance specified by node_id from the database
        """
        linksToDelete = self.get_links_by_origin_node_id(
            node_id
        ) + self.get_links_by_destination_node_id(node_id)
        for link in linksToDelete:
            self.delete_node_link(link.node_link_id)

        self.execute(f"DELETE FROM nodeInstances WHERE node_id = {node_id}")

    def get_links_by_origin_node_id(self, node_id: int) -> list[NodeLink]:
        """
        Returns list of all links that have origin in NodeInstance with specified node_id
        """
        self.check_node_instance_exists(node_id)
        linkRows = self.fetchall_named(
            f"SELECT * FROM nodeLinks WHERE origin_node_id = {node_id}"
        )
        return [NodeLink.fromNameDict(linkRow) for linkRow in linkRows]

    def get_links_by_destination_node_id(self, node_id: int) -> list[NodeLink]:
        """
        Returns list of all links that have destination in NodeInstance with specified node_id
        """
        self.check_node_instance_exists(node_id)
        linkRows = self.fetchall_named(
            f"SELECT * FROM nodeLinks WHERE destination_node_id = {node_id}"
        )
        return [NodeLink.fromNameDict(linkRow) for linkRow in linkRows]

    def get_all_links(
        self,
        origin_node_id: Optional[int] = None,
        destination_node_id: Optional[int] = None,
    ) -> list[NodeLink]:
        """
        Returns all NodeLinks. Can be filtered by origin, and by destination
        """

        # TODO: Simplify this query
        query = "SELECT * FROM nodeLinks "
        if origin_node_id is not None:
            query += f"WHERE origin_node_id = {origin_node_id} "
        if destination_node_id is not None:
            if origin_node_id is not None:
                query += "AND "
            else:
                query += "WHERE "
            query += f"destination_node_id = {destination_node_id} "

        linkRows = self.fetchall_named(query)
        return [NodeLink.fromNameDict(linkRow) for linkRow in linkRows]

    def check_node_link_exists(self, link: NodeLink, raise_on: bool = False) -> None:
        """
        NodeLink is specified by all it's properties (origin, output, input, destination)
        If raise_on == False, will raise if node does not exist
        If raise_on == True, will raise if node does exist
        Otherwise will not do anything
        """

        select_one_query = f"""
            SELECT * FROM nodeLinks
                WHERE origin_node_id = {link.origin_node_id}
                AND destination_node_id = {link.destination_node_id}
                AND destination_node_input = '{link.destination_node_input}'
            """
        if link.origin_node_output is not None:
            select_one_query += f" AND origin_node_output = '{link.origin_node_output}'"
        else:
            select_one_query += " AND origin_node_output IS NULL"

        if self.fetchone(select_one_query) is None:
            if raise_on == False:
                raise ObjectNotInDBException(f"Node link {link.toNameDict()} not found")
        else:
            if raise_on == True:
                raise ObjectAlreadyInDBException(
                    f"Node link {link.toNameDict()} already exists"
                )

    def check_node_link_exists_by_id(
        self, node_link_id: int, raise_on: bool = False
    ) -> None:
        """
        NodeLink is specified by its id
        If raise_on == False, will raise if NodeLink does not exist
        If raise_on == True, will raise if NodeLink does exist
        Otherwise will not do anything
        """
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
        """
        Returns singular NodeLink object, specified by node_link_id
        """
        self.check_node_link_exists_by_id(node_link_id)
        node_row = self.fetchone_named(
            f"SELECT * FROM nodeLinks WHERE node_link_id = {node_link_id}"
        )
        instance = NodeLink.fromNameDict(node_row)
        return instance

    def get_new_node_link_id(self) -> int:
        """
        Generates node_link_id of next NodeLink to be added.
        By default it is MAX(node_link_id)+1
        """
        new_id = self.fetchone("SELECT MAX(node_link_id) FROM nodeLinks")[0]
        if new_id is None:
            new_id = 0
        else:
            new_id += 1
        return new_id

    def create_node_link(self, link: NodeLink) -> int:
        """
        Adds NodeLink object to the database.
        Returns node_link_id of the new NodeLink
        """
        self.check_node_link_exists(link, raise_on=True)
        self.check_node_instance_exists(link.origin_node_id)
        self.check_node_instance_exists(link.destination_node_id)

        node_link_id = self.get_new_node_link_id()

        origin_node_output = (
            link.origin_node_output if link.origin_node_output is not None else "NULL"
        )
        query = f"""
            INSERT INTO nodeLinks
                VALUES (
                    {node_link_id},
                    {link.origin_node_id},
                    {origin_node_output},
                    {link.destination_node_id},
                    '{link.destination_node_input}'
                    )
        """
        self.execute(query)
        return node_link_id

    def update_node_link(self, update_link: NodeLink, to_update_id: int) -> None:
        """
        Overwrites variables of already persisted NodeLink identified by
        to_update_id, with values from update_link
        """
        self.check_node_link_exists_by_id(to_update_id)

        sql_col_eq_values = ", ".join(
            [
                f"{colname}='{value}'"
                for colname, value in update_link.toNameDict().items()
                if value is not None
            ]
        )

        query = f"""
        UPDATE nodeLinks
        SET {sql_col_eq_values}
        WHERE node_link_id = {to_update_id}
        """
        self.execute(query)

    def delete_node_link(self, node_link_id: int) -> None:
        """
        Removes NodeLink identified by node_link_id from the database
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
        """ """
        if node_type_name not in self.get_all_node_type_names():
            if raise_on == False:
                raise ObjectNotInDBException(f"Node type {node_type_name} not found")
        else:
            if raise_on == True:
                raise ObjectAlreadyInDBException(
                    f"Node type {node_type_name} already exists"
                )

    def does_node_have_kwarg(self, node_type_name: str, kwarg_name: str):
        node_type = self.get_node_type_from_name(node_type_name)
        if kwarg_name not in node_type.get_arg_names():
            raise ObjectNotInDBException(
                f"""Nodes of type_name= "{node_type.get_name()}" do not have any argument with kwarg_name="{kwarg_name}\""""
            )

    def get_all_node_type_names(self) -> list[str]:
        return list(NodeType.all_udn.keys())
    
    def get_all_node_types(self) -> list[NodeType]:
        return list(NodeType.all_udn.values())

    def get_node_instance_type_name(self, node_id: int) -> str:
        self.check_node_instance_exists(node_id)
        node_type_name = self.fetchone(
            f"SELECT node_type FROM nodeInstances WHERE node_id = {node_id}"
        )[0]
        return node_type_name

    def get_node_type_from_name(self, node_type_name: str) -> NodeType:
        self.check_node_type_exists(node_type_name)
        return NodeType.all_udn[node_type_name]

    def get_arg_type(self, node_type_name: str, arg_name: str):
        self.does_node_have_kwarg(node_type_name, arg_name)
        return (
            self.get_node_type_from_name(node_type_name).get_arg_types().get(arg_name)
        )

    def get_prerequisite_node_ids(self, node_id: int) -> list[int]:
        self.check_node_instance_exists(node_id)

        node_rows = self.fetchall_named(
            f"""SELECT node_id
            FROM nodeInstances
            JOIN nodeLinks ON origin_node_id = node_id
            WHERE destination_node_id = {node_id}""",
        )

        return [node_row["node_id"] for node_row in node_rows]

    def get_following_node_ids(self, node_id: int) -> list[int]:
        self.check_node_instance_exists(node_id)

        node_rows = self.fetchall_named(
            f"""
            SELECT destination_node_id
            FROM nodeLinks
            WHERE origin_node_id = {node_id}
            """,
        )

        return [node_row["destination_node_id"] for node_row in node_rows]

    def delete_all_following_node_outputs(self, node_id: int) -> list[int]:
        to_remove: list[int] = []
        to_check: list[int] = [node_id]

        while len(to_check) > 0:
            checked = to_check.pop()
            to_remove.append(checked)
            to_check.extend(self.get_following_node_ids(checked))

        for node_id in to_remove:
            if self.is_output_created(node_id):
                self.delete_output(node_id)
