import { useState } from "react";
import { Modal, Button, Table, Card } from "react-bootstrap";
import { useEffect } from "react";
import { getProcessingQueue } from "../services/processingApiService";
interface BlockModalDetailsProps {
  show: boolean;
  handleClose: () => void;
}
const QueueModalDetails = ({ show, handleClose }: BlockModalDetailsProps) => {
  const [processingQueue, setProcessingQueue] = useState<any[]>([]);

  function updateProcessingQueue() {
    console.log("Updating processing queue...");
    getProcessingQueue().then((queue) => {
      setProcessingQueue(queue);
    });
  }

  useEffect(() => {
    let interval: number | null = null;
    if (show) {
      updateProcessingQueue();
      interval = setInterval(updateProcessingQueue, 3000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [show]);

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
        <Button variant="secondary" onClick={() => handleClose()}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default QueueModalDetails;
