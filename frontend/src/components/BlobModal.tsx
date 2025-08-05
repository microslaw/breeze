import { Button, Modal, Image } from "react-bootstrap";
import styles from "./BlobModal.module.css";

interface BlobModalProps {
  show: boolean;
  blobUrl: string;
  handleClose: () => void;
}

const BlobModal = ({ show, blobUrl, handleClose }: BlobModalProps) => {
  return (
    <Modal
      show={show}
      size="lg"
      centered
      className={styles.modal}
      dialogClassName={styles.modalDialog}
    >
      <Modal.Header>
        <Modal.Title>Blob</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Image src={blobUrl} rounded className={styles.image} />
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default BlobModal;
