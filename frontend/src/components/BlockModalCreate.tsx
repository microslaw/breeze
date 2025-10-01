import React, { useEffect, useState } from "react";
import { Modal, Button, Form, ListGroup } from "react-bootstrap";
import { BlockI } from "../models/block.model";
import {
  createNode,
  getAllNodes,
  getNodeTypesEnrichedByColour,
} from "../services/mainApiService";
import { BLOCK_DEFAULT_COLOUR } from "../constants/ui";
import { NodeTypeI } from "../models/nodetype.model";

interface BlockModalCreateProps {
  show: boolean;
  handleClose: () => void;
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
}

const BlockModalCreate = ({
  show,
  handleClose,
  blocks,
  setBlocks,
}: BlockModalCreateProps) => {
  const [block, setBlock] = useState<BlockI>({
    name: "",
    type: "",
    id: -1,
    x: 0,
    y: 0,
    isDragging: false,
    isSelected: false,
    isQueued: false,
    kwargs: [],
    colour: BLOCK_DEFAULT_COLOUR,
  });

  const [blockTypes, setBlockTypes] = useState<NodeTypeI[]>([]);

  useEffect(() => {
    const fetchBlockTypes = async () => {
      const nodeTypes = await getNodeTypesEnrichedByColour();
      nodeTypes.sort((a, b) => a.name.localeCompare(b.name));
      setBlockTypes(nodeTypes);
    };
    fetchBlockTypes();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = e.target;
    setBlock((prevBlock) => ({
      ...prevBlock,
      [name]: name === "x" || name === "y" ? Number(value) : value,
    }));
  };

  const handleSubmit = () => {
    createNode(block).then(async () => {
      setBlock({
        name: "",
        type: "",
        id: -1,
        x: 0,
        y: 0,
        isDragging: false,
        isSelected: false,
        isQueued: false,
        kwargs: [],
        colour: BLOCK_DEFAULT_COLOUR,
      });

      const blocks = await getAllNodes();
      setBlocks(blocks);
    });
    handleClose();
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Create New Block</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group controlId="formBlockName">
            <Form.Label>Name</Form.Label>
            <Form.Control
              as="input"
              type="string"
              name="name"
              value={block.name}
              onChange={handleChange}
            />
          </Form.Group>
          <Form.Group controlId="formBlockType">
            <Form.Label>Type</Form.Label>
            <Form.Select
              as="input"
              type="string"
              name="type"
              value={block.type}
              onChange={handleChange}
            >
              <option value="" disabled>
                Select a type
              </option>
              {blockTypes.map((type) => (
                <option key={type.name} value={type.name}>
                  {type.name.replaceAll("_", " ").toUpperCase() +
                    " (" +
                    type.tags.join(", ") +
                    ")"}
                </option>
              ))}
            </Form.Select>
          </Form.Group>
          {/* Input for block coords on canvas */}
          {/* <Form.Group controlId="formBlockX">
            <Form.Label>X Coordinate</Form.Label>
            <Form.Control
              as="input"
              type="number"
              name="x"
              value={block.x}
              onChange={handleChange}
            />
          </Form.Group>
          <Form.Group controlId="formBlockY">
            <Form.Label>Y Coordinate</Form.Label>
            <Form.Control
              as="input"
              type="number"
              name="y"
              value={block.y}
              onChange={handleChange}
            />
          </Form.Group> */}
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" className="me-auto" onClick={handleClose}>
          Close
        </Button>
        <Button variant="primary" onClick={handleSubmit}>
          Save Changes
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default BlockModalCreate;
