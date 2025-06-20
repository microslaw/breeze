import React, { useEffect, useState } from "react";
import { Modal, Button, Table, Card } from "react-bootstrap";
import { BlockI } from "../models/block.model";
import {
  getProcessingResultByNodeId,
  runProcessingJob,
} from "../services/processingApiService";
import styles from "./BlockModalDetails.module.css";
import {
  getKwargsByNodeId,
  updateKwargByNodeId,
} from "../services/kwargsApiService";
import { KwargI } from "../models/kwarg.model";

interface BlockModalDetailsProps {
  show: boolean;
  block: BlockI;
  setBlock: React.Dispatch<React.SetStateAction<BlockI>>;
  handleClose: () => void;
  handleDelete: (blockId: number) => void;
}

const BlockModalDetails = ({
  show,
  block,
  setBlock,
  handleClose,
  handleDelete,
}: BlockModalDetailsProps) => {
  // TODO put processing result into some kind of structure
  const [processingResult, setProcessingResult] = useState<any>(null);

  const [focusedKwargValue, setFocusedKwargValue] = useState<KwargI>({
    key: "",
    value: "",
    type: "",
    source: "",
  });

  const [errorMsg, setErrorMsg] = useState<string>("");

  useEffect(() => {
    if (!show) return;
    getLastProcessingResult();
    getKwargs();
  }, [show, block.id]);

  useEffect(() => {
    if (errorMsg) {
      const timer = setTimeout(() => setErrorMsg(""), 5000);
      return () => clearTimeout(timer);
    }
  }, [errorMsg]);

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
    getProcessingResultByNodeId(block.id)
      .then((result) => {
        setProcessingResult(result);
      })
      .catch((error) => {
        setErrorMsg(`Processing for block '${block.name}' failed.`);
        console.error("Error fetching processing result:", error);
      });
  };

  const getKwargs = () => {
    getKwargsByNodeId(block.id)
      .then((kwargs) => {
        setBlock((prevBlock) => ({ ...prevBlock, kwargs }));
      })
      .catch((error) => {
        setErrorMsg(`Fetching kwargs for block '${block.name}' failed`);
        console.error("Error fetching kwargs:", error);
      });
  };

  // Called on every input change
  const handleKwargValueChange = (kwargKey: string, newValue: string) => {
    const updatedKwargs = block.kwargs.map((el) =>
      el.key === kwargKey ? { ...el, value: newValue, source: "overwrite" } : el
    );
    setBlock((prevBlock) => ({ ...prevBlock, kwargs: updatedKwargs }));
  };

  // Called when input is focused
  const handleKwargValueFocus = (kwargKey: string, value: string) => {
    setFocusedKwargValue({ ...focusedKwargValue, key: kwargKey, value: value });
  };

  // Called when input loses focus
  const handleKwargValueBlur = (kwarg: KwargI) => {
    const originalValue = focusedKwargValue.value;
    if (originalValue === kwarg.value) {
      return;
    }

    updateKwargByNodeId(block.id, kwarg)
      .then(() => {
        console.log(`Kwarg ${kwarg.key} updated successfully`);
      })
      .catch((error) => {
        const updatedKwargs = block.kwargs.map((el) =>
          el.key === kwarg.key ? { ...el, value: originalValue } : el
        );
        setBlock((prevBlock) => ({ ...prevBlock, kwargs: updatedKwargs }));
        setErrorMsg(
          `Kwarg '${kwarg.key}' value can not be set to: ${kwarg.value}.`
        );
        console.error(`Error updating kwarg ${kwarg.key}:`, error);
      });
  };

  return (
    <Modal show={show}>
      <Modal.Header>
        <Modal.Title>{block.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body className={styles.modalBody}>
        {errorMsg && (
          <div style={{ color: "red", marginBottom: "10px" }}>{errorMsg}</div>
        )}
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
                    <input
                      type="text"
                      value={kwarg.value ?? ""}
                      onChange={(e) =>
                        handleKwargValueChange(kwarg.key, e.target.value)
                      }
                      onFocus={(e) =>
                        handleKwargValueFocus(kwarg.key, kwarg.value)
                      }
                      onBlur={() => handleKwargValueBlur(kwarg)}
                    />
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
