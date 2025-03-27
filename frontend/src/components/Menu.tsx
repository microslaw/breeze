import React, { useState } from "react";
import styles from "./Menu.module.css";
import BlockModalCreate from "./BlockModalCreate";
import { BlockI } from "../models/block.model";
import { Button } from "react-bootstrap";

interface MenuProps {
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
}

const Menu = ({ blocks, setBlocks }: MenuProps) => {
  const [isBlockModalCreateVisible, setIsBlockModalCreateVisible] =
    useState<boolean>(false);

  return (
    <div className={styles.menu}>
      <Button onClick={() => setIsBlockModalCreateVisible(true)}>
        Add new block
      </Button>
      <Button onClick={() => console.log(blocks)}>Log list of blocks</Button>
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
