from flask import Flask, request, testing
from flask_cors import CORS
from backend.datatypes import NodeInstance, NodeLink
from backend.repository import Repository
from backend.repository import ObjectAlreadyInDBException
from backend.repository import ObjectNotInDBException
from backend.processor import Processor, ProcessingException
from backend.formatting import (
    format_for_display,
    format_from_input,
    frontend_display_type,
    get_tag_color_map,
)
from typing import Any


class BadRequestException(Exception):
    """Exception raised for invalid API requests."""

    pass


class Controller:
    """
    Passes API communications to repository or processor.
    Provides REST endpoints for node types, instances, links, processing, and kwargs.
    """

    def __init__(self, repository: Repository, processor: Processor):
        """
        Initialize the Controller with a repository and processor.

        :param repository: repository instance for data access.
        :param processor: processor instance for workflow execution.
        """
        self.flask_server = Flask(__name__)
        CORS(self.flask_server, origins=["http://localhost:5173"])

        self.repository = repository
        self.processor = processor

        @self.flask_server.errorhandler(ObjectNotInDBException)
        def server_error_not_in_db(err: ObjectNotInDBException):
            """
            Handle ObjectNotInDBException errors.

            :param err: Exception instance.
            :return: Error message and 404 status code.
            """
            return str(err), 404

        @self.flask_server.errorhandler(ObjectAlreadyInDBException)
        def server_error_already_in_db(err: ObjectAlreadyInDBException):
            """
            Handle ObjectAlreadyInDBException errors.

            :param err: Exception instance.
            :return: Error message and 409 status code.
            """
            return str(err), 409

        @self.flask_server.errorhandler(ProcessingException)
        def server_error_processing(err: ProcessingException):
            """
            Handle ProcessingException errors.

            :param err: Exception instance.
            :return: Error message and 422 status code.
            """
            self.processor.reset_processing_queue()
            return err.toJson(), 422

        @self.flask_server.errorhandler(BadRequestException)
        def server_error_bad_request(err: BadRequestException):
            """
            Handle BadRequestException errors.

            :param err: Exception instance.
            :return: Error message and 400 status code.
            """
            return str(err), 400

        @self.flask_server.route("/nodeTypes", methods=["GET"])
        def get_all_node_types():
            """
            Returns all node types.

            :return: list of node types.
            """
            return [obj.toJSON() for obj in self.repository.get_all_node_types()]

        @self.flask_server.route("/nodeTypes/<node_type_name>", methods=["GET"])
        def get_node_type(node_type_name: str):
            """
            Get detailed info about node type by name

            :param node_type_name: Name of the node type.
            :return: Node type details as JSON.
            """
            return self.repository.get_node_type_from_name(node_type_name).toJSON()

        @self.flask_server.route("/nodeInstances", methods=["GET"])
        def get_all_node_instances():
            """
            Get all node instances.

            :return: list of node instances as dictionaries.
            """
            return [
                node.toNameDict() for node in self.repository.get_all_node_instances()
            ]

        @self.flask_server.route("/nodeInstances/<node_id>", methods=["GET"])
        def get_node_instance(node_id: int):
            """
            Get a node instance by ID.

            :param node_id: Node instance ID.
            :return: Node instance as dictionary.
            """
            return self.repository.get_node_instance(node_id).toNameDict()

        @self.flask_server.route("/nodeInstances", methods=["POST"])
        def create_node_instance():
            """
            Create a new node instance.

            :return: Dictionary with new node ID.
            """
            node_instance = NodeInstance.fromNameDict(request.json)
            node_id = self.repository.create_node_instance(node_instance)
            response = {"node_id": node_id}
            return response, 200

        @self.flask_server.route("/nodeInstances/<node_instance_id>", methods=["PATCH"])
        def patch_node_instance(node_instance_id: int):
            """
            Update a node instance.

            :param node_instance_id: Node instance ID.
            :return: Status message.
            """
            if "node_id" in request.json:
                raise BadRequestException("Field node_id cannot be patched")

            node_instance_update = NodeInstance.fromNameDict(request.json)
            self.repository.update_node_instance(node_instance_update, node_instance_id)

            return "OK", 200

        @self.flask_server.route("/nodeInstances/<node_id>", methods=["DELETE"])
        def delete_node_instance(node_id: int):
            """
            Delete a node instance.

            :param node_id: Node instance ID.
            :return: Status message.
            """
            self.repository.delete_node_instance(node_id)
            return "OK", 200

        @self.flask_server.route("/nodeLinks/<node_link_id>", methods=["GET"])
        def get_node_link(node_link_id: int):
            """
            Get a node link by ID.

            :param node_link_id: Node link ID.
            :return: Node link as dictionary.
            """
            return self.repository.get_node_link(node_link_id).toNameDict()

        @self.flask_server.route(
            "/nodeInstances/<node_id>/clear_output", methods=["DELETE"]
        )
        def clear_node_output(node_id: int):
            """
            Deletes an output, effectively un-processing specified node
            """
            self.repository.delete_output(node_id)
            return "OK", 200

        @self.flask_server.route("/nodeLinks", methods=["GET"])
        def get_all_node_links():
            """
            Get all node links, optionally filtered by origin or destination node.

            :return: List of node links as dictionaries.
            """
            node_links = self.repository.get_all_links(
                origin_node_id=request.args.get("origin_node_id"),
                destination_node_id=request.args.get("destination_node_id"),
            )

            return [link.toNameDict() for link in node_links]

        @self.flask_server.route("/nodeLinks", methods=["POST"])
        def create_node_link():
            """
            Create a new node link.

            :return: Dictionary with new node link ID.
            """
            node_link = NodeLink.fromNameDict(request.json)
            node_link_id = self.repository.create_node_link(node_link)
            response = {"node_link_id": node_link_id}
            return response, 200

        @self.flask_server.route("/nodeLinks/<node_link_id>", methods=["PATCH"])
        def patch_node_link(node_link_id: int):
            """
            Update a node link.

            :param node_link_id: Node link ID.
            :return: Status message.
            """
            if "node_link_id" in request.json:
                raise BadRequestException("Field node_link_id cannot be patched")

            node_link_update = NodeLink.fromNameDict(request.json)
            self.repository.update_node_link(node_link_update, node_link_id)

            return "OK", 200

        @self.flask_server.route("/nodeLinks/<node_link_id>", methods=["DELETE"])
        def delete_node_link(node_link_id: int):
            """
            Delete a node link.

            :param node_link_id: Node link ID.
            :return: Status message.
            """
            self.repository.delete_node_link(node_link_id)
            return "OK", 200

        @self.flask_server.route("/queueProcessing", methods=["POST"])
        def queue_processing():
            """
            Add a node to the processing queue.

            :return: Status message.
            """
            nodeToProcess = NodeInstance.fromNameDict(request.json)
            self.processor.update_processing_schedule(nodeToProcess.node_id)
            return "OK", 200

        @self.flask_server.route("/queueProcessing/all", methods=["POST"])
        def queue_all():
            """
            Starts processing of everything
            """
            self.processor.run_all()
            return "OK", 200

        @self.flask_server.route("/queueProcessing", methods=["GET"])
        def check_processing_queue():
            """
            Get the current processing queue.

            :return: Processing schedule.
            """
            return self.processor.get_processing_schedule()

        @self.flask_server.route("/processingResult/<node_id>", methods=["GET"])
        def get_processing_result(node_id: int):
            """
            Get the processing result for a node.

            :param node_id: specifies id of a node.
            :return: Formatted processing result.
            """
            return format_for_display(self.repository.read_output(node_id))

        @self.flask_server.route("/processingResult/<node_id>", methods=["DELETE"])
        def delete_processing_result(node_id: int):
            """
            Remove the processing result for a node.

            :param node_id: specifies id of a node.
            """
            self.repository.delete_output(node_id)
            return "OK", 200

        @self.flask_server.route("/processingResult/all", methods=["DELETE"])
        def delete_all_processing_results():
            """
            Remove all processing results.

            :return: [node_id for node_id in removed results].
            """

            processed_node_ids = [
                node_id
                for node_id in self.repository.get_all_node_ids()
                if self.repository.is_output_created(node_id)
            ]

            self.repository.delete_all_outputs()

            return processed_node_ids, "200"

        @self.flask_server.route(
            "/processingResult/<node_id>/metadata", methods=["GET"]
        )
        def get_processing_result_metadata(node_id: int):
            """
            Get metadata for a node's processing result.

            :param node_id: specifies id of a node.
            :return: Metadata dictionary.
            """
            if self.repository.is_output_created(node_id):
                output = self.repository.read_output(node_id)
                return {
                    "is_processed": True,
                    "datatype": format_for_display(type(output)),
                    "created_date": format_for_display(
                        repository.get_output_created_date(node_id)
                    ),
                    "frontend_type": frontend_display_type(output),
                }
            else:
                return {"is_processed": False}

        @self.flask_server.route(
            "/nodeInstances/<node_id>/finalKwargs", methods=["GET"]
        )
        def get_final_kwargs(node_id: int):
            """
            Get final kwargs for a node instance.

            :param node_id: specifies id of a node.
            :return: List of formatted kwargs.
            """
            final_kwargs = processor.get_kwargs_details(
                repository.get_node_instance(node_id)
            )

            formated_kwargs = [
                {
                    "arg_name": key,
                    "value": format_for_display(values["value"]),
                    "arg_source": values["arg_source"],
                    "datatype": format_for_display(values["datatype"]),
                }
                for key, values in final_kwargs.items()
            ]
            return formated_kwargs

        @self.flask_server.route(
            "/nodeInstances/<node_id>/kwargs/<kwarg_name>", methods=["GET"]
        )
        def get_kwarg(node_id: int, kwarg_name: str):
            """
            Get a specific kwarg for a node instance.

            :param node_id: specifies id of a node.
            :param kwarg_name: Kwarg name.
            :return: Formatted kwarg value.
            """
            return format_for_display(repository.read_kwarg(node_id, kwarg_name))

        @self.flask_server.route(
            "/nodeInstances/<node_id>/kwargs/<kwarg_name>", methods=["PUT"]
        )
        def put_node_kwarg(node_id: int, kwarg_name: str):
            """
            Update a kwarg for a node instance.

            :param node_id: specifies id of a node.
            :param kwarg_name: Kwarg name.
            :return: Status message.
            """
            node_type_name = repository.get_node_instance_type_name(node_id)
            arg_type = repository.get_arg_type(node_type_name, kwarg_name)
            repository.write_kwarg(
                format_from_input(request.data, arg_type), node_id, kwarg_name
            )
            return "OK", 200

        @self.flask_server.route("/nodeTypes/colours", methods=["GET"])
        def get_tag_color_json():
            return get_tag_color_map()

    def test_client(self, **kwargs: Any) -> testing.FlaskClient:
        """
        Get a Flask test client for the server.

        :param kwargs: Additional arguments for the test client.
        :return: Flask test client.
        """
        return self.flask_server.test_client(**kwargs)

    def run(self, **kwargs: Any):
        """
        Run the Flask server.

        :param kwargs: Additional arguments for Flask run.
        :return: None
        """
        return self.flask_server.run(**kwargs)
