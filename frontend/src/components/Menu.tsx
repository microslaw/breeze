import React, { useState } from "react";
import styles from "./Menu.module.css";
import BlockModal from "./BlockModal";
import { BlockI } from "../models/block.model";
import { Button } from "react-bootstrap";

interface MenuProps {
    blocks: BlockI[];
    setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
}

const Menu = ({blocks, setBlocks}: MenuProps) => {
    const [isBlockModalVisible, setIsBlockModalVisible] = useState<boolean>(false);
    

    return (
        <div className={styles.menu}>
        
            <Button onClick={() => setIsBlockModalVisible(true)}>Add new block</Button>
            <Button onClick={() => console.log(blocks)}>Log list of blocks</Button>
            <BlockModal 
                show={isBlockModalVisible} 
                handleClose={() => setIsBlockModalVisible(false)}
                blocks={blocks}
                setBlocks={setBlocks}
                >
            </BlockModal>
        
        </div>
    );
};

export default Menu;
