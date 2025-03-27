import React, { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import { BlockI } from "../models/block.model";

interface BlockModalDeatilsProps {
  show: boolean;
  block: BlockI;
  handleClose: () => void;
}

const BlockModalDetails = ({
  show,
  block,
  handleClose,
}: BlockModalDeatilsProps) => {
  const handleRunJob = () => {
    console.info("Running job is not yet supported!");
  };

  return (
    <Modal show={show}>
      <Modal.Header>
        <Modal.Title>{block.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p>elko elko witam ze szczegolow blocka</p>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="primary" onClick={handleRunJob}>
          Run job
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default BlockModalDetails;
