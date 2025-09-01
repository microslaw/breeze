import React from "react";
import styles from "./SmallMenu.module.css";
import { BlockI } from "../models/block.model";
import { Button, Card, Modal } from "react-bootstrap";

interface SmallMenuProps {
  show: boolean;
  position_x: number;
  position_y: number;
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
}

const SmallMenu = ({
  show,
  position_x,
  position_y,
  blocks,
  setBlocks,
}: SmallMenuProps) => {
  const positionStyle: React.CSSProperties = {
    left: position_x,
    top: position_y,
  };

  return (
    show && (
      <div className={styles.smallMenuModal} style={positionStyle}>
        <Card className={styles.menuCard}>
          <Button
            size="sm"
            className={styles.menuButton}
            variant="primary"
            onClick={() => console.log("Add new block")}
          >
            Add new block
          </Button>
          <Button
            size="sm"
            className={styles.menuButtonLast}
            variant="primary"
            onClick={() => console.log("Place holder small menu button")}
          >
            Placeholder
          </Button>
        </Card>
      </div>
    )
  );
};

export default SmallMenu;
