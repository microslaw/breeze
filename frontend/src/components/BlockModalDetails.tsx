import React, { useEffect, useState } from "react";
import { Modal, Button, Table, Card } from "react-bootstrap";
import { BlockI } from "../models/block.model";
import {
  getProcessingResultByNodeId,
  runProcessingJob,
} from "../services/processingApiService";
import styles from "./BlockModalDetails.module.css";
import { getKwargsByNodeId } from "../services/kwargsApiService";

interface BlockModalDetailsProps {
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
}: BlockModalDetailsProps) => {
  // TODO put processing result into some kind of structure
  const [processingResult, setProcessingResult] = useState<any>(null);

  useEffect(() => {
    if (!show) return;
    getLastProcessingResult();
    // TODO make kwargs get loaded every time the modal is opened
    getKwargs();
  }, [show, block.id]);

  const handleRunJob = () => {
    runProcessingJob(block.id).then((result) => {
      console.log("Processing job started:", result);
      let count = 0;
      const intervalId = setInterval(() => {
        getLastProcessingResult();
        count++;
        if (count >= 3) {
          clearInterval(intervalId);
        }
      }, 1000);
    });
  };

  const getLastProcessingResult = () => {
    getProcessingResultByNodeId(block.id).then((result) => {
      setProcessingResult(result);
    });
  };

  const getKwargs = () => {
    getKwargsByNodeId(block.id).then((kwargs) => {
      block.kwargs = kwargs;
    });
  };

  return (
    <Modal show={show}>
      <Modal.Header>
        <Modal.Title>{block.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body className={styles.modalBody}>
        <Card className={styles.card}>
          <Card.Header>Processing Result</Card.Header>
          <Card.Body>
            <Card.Text>
              {processingResult ?? "No processing result available"}
            </Card.Text>
          </Card.Body>
        </Card>
        <div className={styles.tableWrapper}>
          <Table hover responsive>
            <thead>
              <tr>
                <th>Field</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(block)
                .filter(([key]) => key !== "kwargs" && key !== "isDragging")
                .map(([key, value]) => (
                  <tr key={key}>
                    <td>{key}</td>
                    <td>{String(value)}</td>
                  </tr>
                ))}
            </tbody>
          </Table>
        </div>
        <div className={styles.tableWrapper}>
          <Table hover responsive>
            <thead>
              <tr>
                <th>Field</th>
                <th>Value</th>
                <th>Type</th>
                <th>Source</th>
              </tr>
            </thead>
            <tbody>
              {block.kwargs.map((kwarg, index) => (
                <tr key={index}>
                  <td>{kwarg.key}</td>
                  <td>
                    {kwarg.value || <i className={styles.emptyTag}>Empty</i>}
                  </td>
                  <td>{kwarg.type}</td>
                  <td>{kwarg.source}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="primary" onClick={handleRunJob}>
          Run job
        </Button>
        <Button variant="danger" onClick={() => handleDelete(block.id)}>
          Delete
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default BlockModalDetails;
