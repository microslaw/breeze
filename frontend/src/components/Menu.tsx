import React, { useState } from "react";
import styles from "./Menu.module.css";
import BlockModalCreate from "./BlockModalCreate";
import { BlockI } from "../models/block.model";
import { Button } from "react-bootstrap";
import {
  getNodeTypes,
  getAllNodes,
  getNodeById,
  getAllLinks,
  getLinksByOriginNode,
  createNode,
} from "../services/mainApiService";
import {
  getProcessingQueue,
  getProcessingResultMetadataByNodeId,
} from "../services/processingApiService";
import QueueModalDetails from "./QueueModalDetails";

interface MenuProps {
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
}

const Menu = ({ blocks, setBlocks }: MenuProps) => {
  const [isBlockModalCreateVisible, setIsBlockModalCreateVisible] =
    useState<boolean>(false);

  const [isQueueModalDeatilsVisible, setIsQueueModalDeatilsVisible] =
    useState<boolean>(false);

  return (
    <div className={styles.menu}>
      {/* Button section for testing purposes only */}
      <span>
        <Button onClick={() => setIsBlockModalCreateVisible(true)}>
          Add new block
        </Button>
        <Button onClick={() => setIsQueueModalDeatilsVisible(true)}>
          View processing queue
        </Button>
      </span>
      <BlockModalCreate
        show={isBlockModalCreateVisible}
        handleClose={() => setIsBlockModalCreateVisible(false)}
        blocks={blocks}
        setBlocks={setBlocks}
      ></BlockModalCreate>
      <QueueModalDetails
        show={isQueueModalDeatilsVisible}
        handleClose={() => setIsQueueModalDeatilsVisible(false)}
      ></QueueModalDetails>
    </div>
  );
};

export default Menu;
