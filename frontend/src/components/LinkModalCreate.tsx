import { useEffect, useState } from "react";
import { LinkI } from "../models/link.model";
import { Modal, Button, Table } from "react-bootstrap";
import { KwargI } from "../models/kwarg.model";
import { getKwargsByNodeId } from "../services/kwargsApiService";
import { createLink, getAllLinks } from "../services/mainApiService";
import assignLinksPositionByBlocksPosition from "../functions/assignLinksPositionByBlocksPosition";
import { BlockI } from "../models/block.model";
import styles from "./LinkModalCreate.module.css";

interface LinkModalCreateProps {
  show: boolean;
  blocks: BlockI[];
  link: LinkI;
  setLinks: React.Dispatch<React.SetStateAction<LinkI[]>>;
  handleClose: () => void;
}

const LinkModalCreate = ({
  show,
  blocks,
  link,
  setLinks,
  handleClose,
}: LinkModalCreateProps) => {
  const [selectedKwarg, setSelectedKwarg] = useState<string | null>(null);
  const [outputNodeKwargs, setOutputNodeKwargs] = useState<KwargI[]>([]);

  useEffect(() => {
    if (show) {
      const fetchAppState = async () => {
        const fetchedKwargs = await getKwargsByNodeId(link.destinationNodeId);
        console.log(
          "Fetched kwargs for node:",
          link.destinationNodeId,
          fetchedKwargs
        );
        setOutputNodeKwargs(fetchedKwargs);
      };
      fetchAppState();
    }
  }, [show]);

  function handleConfirm() {
    link.destinationNodeInput = selectedKwarg || "";
    createLink(link).then((res) => {
      getAllLinks().then((links) => {
        setLinks(links);
        assignLinksPositionByBlocksPosition(blocks, links);
      });
    });
    handleClose();
  }

  function handleKwargChange(event: React.ChangeEvent<HTMLInputElement>) {
    setSelectedKwarg(event.target.value);
  }

  return (
    <Modal show={show} className={styles.modal} size="lg" centered>
      <Modal.Header>
        <Modal.Title>Select destination node input kwarg</Modal.Title>
      </Modal.Header>
      <Modal.Body className={styles.modalBody}>
        {outputNodeKwargs.length > 0 ? (
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Kwarg Key</th>
                <th>Kwarg Value</th>
                <th>Kwarg Type</th>
                <th>Select</th>
              </tr>
            </thead>
            <tbody>
              {outputNodeKwargs.map((kwarg) => (
                <tr key={kwarg.key}>
                  <td>{kwarg.key}</td>
                  <td>{kwarg.value}</td>
                  <td>{kwarg.type}</td>
                  <td className={styles.radioInputTableCell}>
                    <input
                      type="radio"
                      name="kwarg"
                      value={kwarg.key}
                      checked={selectedKwarg === kwarg.key}
                      onChange={handleKwargChange}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        ) : (
          <p>No kwargs available.</p>
        )}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="danger" onClick={() => handleConfirm()}>
          Confirm
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default LinkModalCreate;
