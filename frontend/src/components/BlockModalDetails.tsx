import React, { useEffect, useState } from "react";
import { Modal, Button, Table, Card } from "react-bootstrap";
import { BlockI } from "../models/block.model";
import {
  getProcessingResultByNodeId,
  getProcessingResultMetadataByNodeId,
  runProcessingJob,
} from "../services/processingApiService";
import styles from "./BlockModalDetails.module.css";
import {
  getKwargsByNodeId,
  updateKwargByNodeId,
} from "../services/kwargsApiService";
import { KwargI } from "../models/kwarg.model";
import { ProcessingResultMetadataI } from "../models/processingresultmetadata.model";
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
  const [processingResult, setProcessingResult] = useState<any>(null);

  const [processingResultMetadata, setProcessingResultMetadata] =
    useState<ProcessingResultMetadataI>({
      is_processed: false,
    });

  const [focusedKwargValue, setFocusedKwargValue] = useState<KwargI>({
    key: "",
    value: "",
    type: "",
    source: "",
  });

  const [errorMsg, setErrorMsg] = useState<string>("");

  useEffect(() => {
    if (!show) {
      setProcessingResultMetadata({ is_processed: false });
      setProcessingResult(null);
      setFocusedKwargValue({ key: "", value: "", type: "", source: "" });
      setErrorMsg("");
    } else {
      getProcessingResultMetadataByNodeId(block.id).then((result) => {
        setProcessingResultMetadata(result);
        if (result.is_processed) {
          getProcessingResultByNodeId(block.id).then((result) => {
            setProcessingResult(result);
          });
        }
      });

      getAndAssignKwargs();
    }
  }, [show, block.id]);

  useEffect(() => {
    if (errorMsg) {
      const timer = setTimeout(() => setErrorMsg(""), 5000);
      return () => clearTimeout(timer);
    }
  }, [errorMsg]);

  const handleRunJob = () => {
    runProcessingJob(block.id).then(() => {
      let count = 0;
      const intervalId = setInterval(() => {
        getProcessingResultMetadataByNodeId(block.id).then((result) => {
          setProcessingResultMetadata(result);
          if (result.is_processed) {
            getProcessingResultByNodeId(block.id).then((result) => {
              setProcessingResult(result);
              count++;
              if (
                count >= 3 ||
                processingResultMetadata.is_processed ||
                show === false
              ) {
                clearInterval(intervalId);
              }
            });
          }
        });
      }, 1000);
    });
  };

  const getAndAssignKwargs = () => {
    getKwargsByNodeId(block.id).then((kwargs) => {
      setBlock((prevBlock) => ({ ...prevBlock, kwargs }));
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

  function renderProcessingResult() {
    if (!processingResultMetadata.is_processed) {
      return (
        <Card.Body>
          <Card.Text>No processing result available</Card.Text>
        </Card.Body>
      );
    }
    if (
      processingResultMetadata.frontend_type === "html" ||
      processingResultMetadata.frontend_type === "plaintext"
    ) {
      return (
        <Card.Body>
          <Button
            variant="primary"
            onClick={() => {
              const newWindow = window.open("", "_blank");
              if (newWindow) {
                newWindow.document.writeln(`
                  <html>
                  <head><title>${
                    "Processing result for node: " + block.id
                  }</title><link rel="stylesheet" type="text/css" href="src/components/ProcessingResult.module.css"></head>
                  <body>
                    ${processingResult}
                  </body>
                  </html>
                `);
              }
            }}
          >
            Open Result in New Window
          </Button>
          <Card.Text>
            Processed at:{" "}
            {processingResultMetadata?.created_date
              ? processingResultMetadata?.created_date
              : "no data"}
          </Card.Text>
        </Card.Body>
      );
    }
    return <Card.Text>{processingResult}</Card.Text>;
  }

  return (
    <Modal
      show={show}
      size="lg"
      centered
      className={styles.modal}
      dialogClassName={styles.modalDialog}
    >
      <Modal.Header>
        <Modal.Title>{block.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body className={styles.modalBody}>
        {errorMsg && (
          <div style={{ color: "red", marginBottom: "10px" }}>{errorMsg}</div>
        )}
        <Card className={styles.card}>
          <Card.Header>Processing Result</Card.Header>
          {renderProcessingResult()}
        </Card>
        {/* BLOCK TABLE (test/debug only) */}
        {/* <div className={styles.tableWrapper}>
          <Table hover>
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
        </div> */}
        {/* KWARG TABLE */}
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
                      className={styles.kwargTextInput}
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
