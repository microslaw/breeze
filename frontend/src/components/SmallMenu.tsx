import React from "react";
import styles from "./SmallMenu.module.css";
import { BlockI } from "../models/block.model";
import { Button, Card, Modal } from "react-bootstrap";
import { processAllNodes } from "../services/processingApiService";

interface SmallMenuProps {
  show: boolean;
  setShow: React.Dispatch<React.SetStateAction<boolean>>;
  position_x: number;
  position_y: number;
  setIsBlockModalCreateVisible: React.Dispatch<React.SetStateAction<boolean>>;
}

const SmallMenu = ({
  show,
  setShow,
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
          className={styles.menuButtonLast}
          variant="primary"
          onClick={() => handleProcessAllNodes()}
        >
          Run all nodes
        </Button>
      </Card>
    </div>
  ) : null;
};

export default SmallMenu;
