import React, { useEffect, useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import { BlockI } from "../models/block.model";
import { createNode, getNodeTypes } from "../services/mainApiService";

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
    id: 999,
    x: 0,
    y: 0,
    isDragging: false,
  });

  const [blockTypes, setBlockTypes] = useState<string[]>([]);

  useEffect(() => {
    console.log("BlockModalCreate mounted");
    const fetchBlockTypes = async () => {
      const nodeTypes = await getNodeTypes();
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
    block.id = Math.floor(Math.random() * 1000000);
    setBlocks([...blocks, block]);
    setBlock({
      name: "",
      type: "default",
      id: Math.floor(Math.random() * 1000000),
      x: 0,
      y: 0,
      isDragging: false,
    });
    createNode(block).then((response) => {
      console.log(response);
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
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </Form.Select>
          </Form.Group>
          <Form.Group controlId="formBlockX">
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
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
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
