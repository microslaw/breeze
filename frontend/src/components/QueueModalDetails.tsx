import { Modal, Button } from "react-bootstrap";
import { useEffect } from "react";

interface BlockModalDetailsProps {
  show: boolean;
  handleClose: () => void;
  processingQueue: number[];
}
const QueueModalDetails = ({
  show,
  handleClose,
  processingQueue,
}: BlockModalDetailsProps) => {
  useEffect(() => {}, [show]);

  return (
    <Modal show={show}>
      <Modal.Header>
        <Modal.Title>Processing Queue</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <ul>
          {processingQueue.map((item, idx) => (
            <li key={idx}>{JSON.stringify(item)}</li>
          ))}
        </ul>
      </Modal.Body>
      <Modal.Footer>
        <Button
          variant="secondary"
          className="me-auto"
          onClick={() => handleClose()}
        >
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default QueueModalDetails;
