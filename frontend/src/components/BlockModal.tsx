import React, { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import { BlockI } from "../models/block.model";
import { v4 as uuidv4 } from "uuid";

interface BlockModalProps {
  show: boolean;
  handleClose: () => void;
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
}

const BlockModal = ({
  show,
  handleClose,
  blocks,
  setBlocks,
}: BlockModalProps) => {
  const [block, setBlock] = useState<BlockI>({
    name: "",
    id: "",
    x: 0,
    y: 0,
    isDragging: false,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setBlock((prevBlock) => ({
      ...prevBlock,
      [name]: name === "x" || name === "y" ? Number(value) : value,
    }));
  };

  const handleSubmit = () => {
    block.id = uuidv4();
    console.log(block);
    setBlocks([...blocks, block]);
    setBlock({ name: "", id: "", x: 0, y: 0, isDragging: false });
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

export default BlockModal;
