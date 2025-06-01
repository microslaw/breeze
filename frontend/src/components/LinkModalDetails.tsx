import { LinkI } from "../models/link.model";
import { Modal, Button, Table } from "react-bootstrap";

interface LinkModalDetailsProps {
  show: boolean;
  link: LinkI;
  handleClose: () => void;
  handleDelete: (linkId: number) => void;
}

const LinkModalDetails = ({
  show,
  link,
  handleClose,
  handleDelete,
}: LinkModalDetailsProps) => {
  return (
    <Modal show={show}>
      <Modal.Header>
        <Modal.Title>{link.destinationNodeId}</Modal.Title>
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
            {Object.entries(link).map(([key, value]) => (
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
        <Button variant="danger" onClick={() => handleDelete(0)}>
          Delete
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default LinkModalDetails;
