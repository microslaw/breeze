import React from "react";
import { Button, Card } from "react-bootstrap";
import styles from "./ZoomButtons.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faMagnifyingGlassMinus,
  faMagnifyingGlassPlus,
  faQuestion,
} from "@fortawesome/free-solid-svg-icons";

interface ZoomButtonsProps {}

const ZoomButtons = () => {
  return (
    <div className={styles.zoomButtons}>
      <Card className={styles.buttonsCard}>
        <Button variant="secondary" className={styles.topButton}>
          {" "}
          <FontAwesomeIcon size="xs" icon={faMagnifyingGlassPlus} />
        </Button>
        <Button variant="secondary" className={styles.bottomButton}>
          {" "}
          <FontAwesomeIcon size="xs" icon={faMagnifyingGlassMinus} />
        </Button>
      </Card>
    </div>
  );
};

export default ZoomButtons;
