import React from "react";
import styles from "./Menu.module.css";
import Button from "./Button";

const Menu = () => {
  return (
    <div className={styles.menu}>
      <ul>
        <Button content="Add new block" onClick={function (): void {
          throw new Error("Function not implemented.");
        } } />
      </ul>
    </div>
  );
};

export default Menu;
