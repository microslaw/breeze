import React, { useEffect, useState } from "react";
import {
  Modal,
  Button,
  Table,
  Card,
  OverlayTrigger,
  Tooltip,
} from "react-bootstrap";
import { BlockI } from "../models/block.model";
import {
  clearProcessingException,
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
import { FrontendTypeEnum } from "../types/frontendType";
import { faTrashCan, faRotate } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import checkForExceptionByNodeId from "../functions/checkForExceptionByNodeId";
interface BlockModalDetailsProps {
  show: boolean;
  block: BlockI;
  setBlock: React.Dispatch<React.SetStateAction<BlockI>>;
  handleClose: () => void;
  handleDelete: (blockId: number) => void;
  handleDeleteProcessingResult: (blockId: number) => Promise<void>;
}

const BlockModalDetails = ({
  show,
  block,
  setBlock,
  handleClose,
  handleDelete,
  handleDeleteProcessingResult,
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
      getProcessingResultAndProcessingResultMetadata();
      getAndAssignKwargs();
    }
  }, [show, block.id]);

  useEffect(() => {
    if (errorMsg) {
      const timer = setTimeout(() => setErrorMsg(""), 5000);
      return () => clearTimeout(timer);
    }
  }, [errorMsg]);

  useEffect(() => {
    if (block.isProcessed) {
      getProcessingResultMetadataByNodeId(block.id).then((result) => {
        setProcessingResultMetadata(result);
        if (result.is_processed) {
          getProcessingResultByNodeId(block.id).then((result) => {
            setProcessingResult(result);
          });
        }
      });
    }
  }, [block.isProcessed]);

  const getProcessingResultAndProcessingResultMetadata = () => {
    checkForExceptionByNodeId(block.id).then((e) => {
      if (e) {
        setProcessingResultMetadata({
          is_processed: false,
          frontend_type: FrontendTypeEnum.ERROR,
        });
        setProcessingResult(e);
      } else {
        getProcessingResultMetadataByNodeId(block.id).then((result) => {
          setProcessingResultMetadata(result);
          if (result.is_processed) {
            block.isProcessed = true;
            getProcessingResultByNodeId(block.id).then((result) => {
              setProcessingResult(result);
            });
          } else {
            block.isProcessed = false;
          }
        });
      }
    });
  };

  const renderTooltipClear = (props: any) => (
    <Tooltip id="button-tooltip" {...props}>
      Clear processing result
    </Tooltip>
  );

  const renderTooltipRefresh = (props: any) => (
    <Tooltip id="button-tooltip" {...props}>
      Refresh processing result
    </Tooltip>
  );

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

  function renderModalTitle() {
    if (block.name) {
      return <Modal.Title>{block.name.replaceAll("_", " ")}</Modal.Title>;
    } else if (block.type) {
      return <Modal.Title>{block.type}</Modal.Title>;
    } else {
      return <Modal.Title>Unknown name and type</Modal.Title>;
    }
  }

  function renderProcessingResult() {
    if (processingResultMetadata.frontend_type === FrontendTypeEnum.ERROR) {
      return (
        <Card.Body>
          <Card.Text className={styles.errorText}>{processingResult}</Card.Text>
        </Card.Body>
      );
    }
    if (!processingResultMetadata.is_processed) {
      return (
        <Card.Body>
          <Card.Text>No processing result available</Card.Text>
        </Card.Body>
      );
    }
    if (processingResultMetadata.frontend_type === FrontendTypeEnum.HtmlDiv) {
      return (
        <Card.Body>
          <div
            className={styles.processingResult}
            dangerouslySetInnerHTML={{ __html: processingResult }}
          />
          <Card.Text className={styles.processedAt}>
            Processed at:{" "}
            <span className={styles.processedAtDate}>
              {processingResultMetadata?.created_date
                ? processingResultMetadata?.created_date
                : "no data"}
            </span>
          </Card.Text>
        </Card.Body>
      );
    } else if (
      processingResultMetadata.frontend_type === FrontendTypeEnum.HtmlWebsite
    ) {
      return (
        <Card.Body>
          <Button
            className={styles.newWindowButton}
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
          <Card.Text className={styles.processedAt}>
            Processed at:{" "}
            <span className={styles.processedAtDate}>
              {processingResultMetadata?.created_date
                ? processingResultMetadata?.created_date
                : "no data"}
            </span>
          </Card.Text>
        </Card.Body>
      );
    }
    return (
      <Card.Body>
        <Card.Text>{processingResult}</Card.Text>
        <Card.Text className={styles.processedAt}>
          Processed at:{" "}
          <span className={styles.processedAtDate}>
            {processingResultMetadata?.created_date
              ? processingResultMetadata?.created_date
              : "no data"}
          </span>
        </Card.Text>
      </Card.Body>
    );
  }

  return (
    <Modal
      show={show}
      size="lg"
      centered
      className={styles.modal}
      dialogClassName={styles.modalDialog}
    >
      <Modal.Header>{renderModalTitle()}</Modal.Header>
      <Modal.Body className={styles.modalBody}>
        {errorMsg && (
          <div style={{ color: "red", marginBottom: "10px" }}>{errorMsg}</div>
        )}
        <Card className={styles.card}>
          <Card.Header
            className="d-flex align-items-center"
            style={{ height: "70px" }}
          >
            <p className="me-auto mb-0 fs-5">Processing Result</p>
            <OverlayTrigger
              placement="right"
              delay={{ show: 100, hide: 150 }}
              overlay={renderTooltipRefresh}
            >
              <Button
                variant="secondary"
                style={{
                  borderRadius: "50%",
                  width: "40px",
                  height: "40px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  padding: 0,
                }}
                onClick={() => {
                  getProcessingResultAndProcessingResultMetadata();
                }}
              >
                <FontAwesomeIcon icon={faRotate} />
              </Button>
            </OverlayTrigger>
            {(block.isProcessed ||
              processingResultMetadata.frontend_type ===
                FrontendTypeEnum.ERROR) && (
              <div className="my-2 ms-2">
                <OverlayTrigger
                  placement="right"
                  delay={{ show: 100, hide: 150 }}
                  overlay={renderTooltipClear}
                >
                  <Button
                    variant="danger"
                    style={{
                      borderRadius: "50%",
                      width: "40px",
                      height: "40px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      padding: 0,
                    }}
                    onClick={() => {
                      if (
                        processingResultMetadata.frontend_type ===
                        FrontendTypeEnum.ERROR
                      ) {
                        clearProcessingException().then(() => {
                          setProcessingResult(null);
                          setProcessingResultMetadata({
                            is_processed: false,
                          });
                        });
                      } else if (block.isProcessed) {
                        handleDeleteProcessingResult(block.id).then(() => {
                          getProcessingResultAndProcessingResultMetadata();
                        });
                      }
                    }}
                  >
                    <FontAwesomeIcon icon={faTrashCan} />
                  </Button>
                </OverlayTrigger>
              </div>
            )}
          </Card.Header>
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
        {/* TODO move to separate component */}
        {block.kwargs.length > 0 && (
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
        )}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" className="me-auto" onClick={handleClose}>
          Close
        </Button>
        <Button
          variant="primary"
          onClick={() => {
            runProcessingJob(block.id);
          }}
        >
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
