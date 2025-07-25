import { useEffect } from "react";
import { LinkI } from "../models/link.model";
import { Modal, Button, Table } from "react-bootstrap";
import { KwargI } from "../models/kwarg.model";
import { getKwargsByNodeId } from "../services/kwargsApiService";
import { createLink, getAllLinks } from "../services/mainApiService";
import assignLinksPositionByBlocksPosition from "../functions/assignLinksPositionByBlocksPosition";
import { BlockI } from "../models/block.model";

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
    console.log("Link confirmed:", link);
    createLink(link).then((res) => {
      getAllLinks().then((links) => {
        setLinks(links);
        assignLinksPositionByBlocksPosition(blocks, links);
      });
    });
    handleClose();
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
        <Button variant="danger" onClick={() => handleConfirm()}>
          Confirm
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default LinkModalCreate;
