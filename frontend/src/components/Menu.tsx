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
import { getProcessingQueue } from "../services/processingApiService";
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
        {/* Comented out functions are used for testing purposes do not remove
        them !!! */}
        {/* <Button onClick={() => console.log(blocks)}>Log list of blocks</Button>
        <Button onClick={() => getNodeTypes()}>Get node types from API</Button>
        <Button onClick={() => getAllNodes()}>
          Get node instances from API
        </Button>
        <Button onClick={() => getNodeById(1)}>
          Get node instance by ID from API
        </Button>
        <Button onClick={() => getLinksByOriginNode(1)}>
        Get node links by origin ID from API
        </Button>
        <Button onClick={() => getAllLinks()}>Get node links from API</Button> */}
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
