import styles from "./Menu.module.css";
import { BlockI } from "../models/block.model";
import { Badge, Button, ListGroup } from "react-bootstrap";

interface MenuProps {
  processingQueue: number[];
  blocks: BlockI[];
  setIsBlockModalCreateVisible: React.Dispatch<React.SetStateAction<boolean>>;
  setIsQueueModalDetailsVisible: React.Dispatch<React.SetStateAction<boolean>>;
}

const Menu = ({
  processingQueue,
  blocks,
  setIsBlockModalCreateVisible,
  setIsQueueModalDetailsVisible,
}: MenuProps) => {
  return (
    <div className={styles.menu}>
      <span>
        <Button onClick={() => setIsBlockModalCreateVisible(true)}>
          Add new block
        </Button>
        {/* <Button onClick={() => setIsQueueModalDetailsVisible(true)}>
          View processing queue
        </Button> */}
      </span>
      <h5 className={styles.queueHeader}>Processing Queue</h5>
      {processingQueue.length !== 0 ? (
        <div>
          <div className={styles.scrollableListGroup}>
            <ListGroup>
              {processingQueue.map((queuedBlockId) => (
                <ListGroup.Item
                  className="d-flex justify-content-between align-items-start"
                  key={queuedBlockId}
                  style={{ wordBreak: "break-word" }}
                >
                  <span>{blocks[queuedBlockId].name}</span>
                  <small
                    style={{
                      backgroundColor: blocks[queuedBlockId].colour,
                      color: "black",
                      borderRadius: "12px",
                      padding: "2px 8px",
                      fontSize: "12px",
                      width: "30px",
                      textAlign: "center",
                    }}
                  >
                    {queuedBlockId}
                  </small>
                </ListGroup.Item>
              ))}
            </ListGroup>
          </div>
        </div>
      ) : (
        <div
          className={styles.queueHeader}
          style={{ marginTop: 20, color: "#666", textAlign: "center" }}
        >
          Processing queue is empty.
        </div>
      )}
    </div>
  );
};

export default Menu;
