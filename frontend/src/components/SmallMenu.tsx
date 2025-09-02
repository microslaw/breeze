import React from "react";
import styles from "./SmallMenu.module.css";
import { BlockI } from "../models/block.model";
import { Button, Card, Modal } from "react-bootstrap";

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
  ) : null;
};

export default SmallMenu;
