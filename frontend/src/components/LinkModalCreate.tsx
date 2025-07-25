import { useEffect } from "react";
import { LinkI } from "../models/link.model";
import { Modal, Button, Table } from "react-bootstrap";
import { KwargI } from "../models/kwarg.model";
import { getKwargsByNodeId } from "../services/kwargsApiService";

interface LinkModalCreateProps {
  show: boolean;
  link: LinkI;
  handleClose: () => void;
}

const LinkModalCreate = ({ show, link, handleClose }: LinkModalCreateProps) => {
  useEffect(() => {
    if (show) {
      const fetchAppState = async () => {
        outputNodeKwargs = await getKwargsByNodeId(link.destinationNodeId);
        console.log(
          "Fetched kwargs for node:",
          link.destinationNodeId,
          outputNodeKwargs
        );
      };
      fetchAppState();
    }
  }, [show]);

  let outputNodeKwargs: KwargI[] = [];

  function handleConfirm() {
    return () => {
      console.log("Link confirmed:", link);
      handleClose();
    };
  }

  return (
    <Modal show={show}>
      <Modal.Header>
        <Modal.Title>elkoelko</Modal.Title>
      </Modal.Header>
      <Modal.Body></Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="danger" onClick={handleConfirm()}>
          Confirm
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default LinkModalCreate;
