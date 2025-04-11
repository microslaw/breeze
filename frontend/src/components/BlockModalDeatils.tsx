import React, { useState } from "react";
import { Modal, Button, Table } from "react-bootstrap";
import { BlockI } from "../models/block.model";

interface BlockModalDeatilsProps {
  show: boolean;
  block: BlockI;
  handleClose: () => void;
  handleDelete: (blockId: number) => void;
}

const BlockModalDetails = ({
  show,
  block,
  handleClose,
  handleDelete,
}: BlockModalDeatilsProps) => {
  const handleSaveChanges = () => {
    console.info("Running job is not yet supported!");
  };

  return (
    <Modal show={show}>
      <Modal.Header>
        <Modal.Title>{block.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Table hover bordered>
          <thead>
            <tr>
              <th>Field</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(block).map(([key, value]) => (
              <tr key={key}>
                <td>{key}</td>
                <td>{String(value)}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="primary" onClick={handleSaveChanges}>
          Save changes
        </Button>
        <Button variant="danger" onClick={() => handleDelete(block.id)}>
          Delete
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default BlockModalDetails;
