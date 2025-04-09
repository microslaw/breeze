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
} from "../services/mainApiService";

interface MenuProps {
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
}

const Menu = ({ blocks, setBlocks }: MenuProps) => {
  const [isBlockModalCreateVisible, setIsBlockModalCreateVisible] =
    useState<boolean>(false);

  return (
    <div className={styles.menu}>
      {/* Button section for testing purposes only */}
      <span>
        <Button onClick={() => setIsBlockModalCreateVisible(true)}>
          Add new block
        </Button>
        <Button onClick={() => console.log(blocks)}>Log list of blocks</Button>
        <Button onClick={() => getNodeTypes()}>Get node types from API</Button>
        <Button onClick={() => getAllNodes()}>
          Get node instances from API
        </Button>
        <Button onClick={() => getNodeById(1)}>
          Get node instance by ID from API
        </Button>
        <Button onClick={() => getAllLinks()}>Get node links from API</Button>
        <Button onClick={() => getLinksByOriginNode(1)}>
          Get node links by origin ID from API
        </Button>
      </span>
      <BlockModalCreate
        show={isBlockModalCreateVisible}
        handleClose={() => setIsBlockModalCreateVisible(false)}
        blocks={blocks}
        setBlocks={setBlocks}
      ></BlockModalCreate>
    </div>
  );
};

export default Menu;
