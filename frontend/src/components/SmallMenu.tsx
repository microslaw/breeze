import React from "react";
import styles from "./SmallMenu.module.css";
import { BlockI } from "../models/block.model";
import { Button, Card, Modal } from "react-bootstrap";
import {
  deleteProcessingResultForAllNodes,
  processAllNodes,
} from "../services/processingApiService";

interface SmallMenuProps {
  show: boolean;
  setShow: React.Dispatch<React.SetStateAction<boolean>>;
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
  position_x: number;
  position_y: number;
  setIsBlockModalCreateVisible: React.Dispatch<React.SetStateAction<boolean>>;
}

const SmallMenu = ({
  show,
  setShow,
  setBlocks,
  position_x,
  position_y,
  setIsBlockModalCreateVisible,
}: SmallMenuProps) => {
  const positionStyle: React.CSSProperties = {
    left: position_x,
    top: position_y,
  };

  function handleProcessAllNodes() {
    processAllNodes();
    // .then((res) => {
    //   console.log("all nodes added to processing queue", res);
    // });
  }

  function handleClearResults() {
    deleteProcessingResultForAllNodes().then(() => {
      setBlocks((prevBlocks) =>
        prevBlocks.map((block) => ({ ...block, isProcessed: false }))
      );
    });
  }

  return show ? (
    <div className={styles.smallMenuModal} style={positionStyle}>
      <Card className={styles.menuCard}>
        <Button
          size="sm"
          className={styles.menuButton}
          variant="primary"
          onClick={() => {
            setShow(false);
            setIsBlockModalCreateVisible(true);
          }}
        >
          Add new node
        </Button>
        <Button
          size="sm"
          className={styles.menuButton}
          variant="primary"
          onClick={() => handleProcessAllNodes()}
        >
          Run all nodes
        </Button>
        <Button
          size="sm"
          className={styles.menuButtonLast}
          variant="danger"
          onClick={() => handleClearResults()}
        >
          Clear results
        </Button>
      </Card>
    </div>
  ) : null;
};

export default SmallMenu;
