import React, { useState } from "react";
import styles from "./Menu.module.css";
import BlockModalCreate from "./BlockModalCreate";
import { BlockI } from "../models/block.model";
import { Button } from "react-bootstrap";
import QueueModalDetails from "./QueueModalDetails";

interface MenuProps {
  setIsBlockModalCreateVisible: React.Dispatch<React.SetStateAction<boolean>>;
}

const Menu = ({ setIsBlockModalCreateVisible }: MenuProps) => {
  const [isQueueModalDetailsVisible, setIsQueueModalDetailsVisible] =
    useState<boolean>(false);

  return (
    <div className={styles.menu}>
      <span>
        <Button onClick={() => setIsBlockModalCreateVisible(true)}>
          Add new block
        </Button>
        <Button onClick={() => setIsQueueModalDetailsVisible(true)}>
          View processing queue
        </Button>
      </span>
      {/* TODO move QueueModalDetails to App */}
      <QueueModalDetails
        show={isQueueModalDetailsVisible}
        handleClose={() => setIsQueueModalDetailsVisible(false)}
      ></QueueModalDetails>
    </div>
  );
};

export default Menu;
