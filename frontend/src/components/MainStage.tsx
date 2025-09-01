import React, { useState } from "react";
import { Stage } from "react-konva";
import FlowLayer from "./FlowLayer";
import { BlockI } from "../models/block.model";
import { LinkI } from "../models/link.model";
import styles from "./MainStage.module.css";
import SmallMenu from "./SmallMenu";

interface MainStageProps {
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
  links: LinkI[];
  setLinks: React.Dispatch<React.SetStateAction<LinkI[]>>;
  setSelectedLink: React.Dispatch<React.SetStateAction<LinkI>>;
  setIsLinkModalCreateVisible: React.Dispatch<React.SetStateAction<boolean>>;
  handleBlockDoubleClick: (block: BlockI) => void;
  handleLinkDoubleClick: (link: LinkI) => void;
}

const MainStage = ({
  blocks,
  setBlocks,
  links,
  setLinks,
  setSelectedLink,
  setIsLinkModalCreateVisible,
  handleBlockDoubleClick,
  handleLinkDoubleClick,
}: MainStageProps) => {
  const [isSmallMenuVisible, setIsSmallMenuVisible] = useState<boolean>(false);
  const [lastClickPosition, setLastClickPosition] = useState<{
    x: number;
    y: number;
  }>({ x: 0, y: 0 });

  function handleClick(e: any) {
    if (e.target !== e.target.getStage()) return;

    setLastClickPosition({ x: e.evt.layerX, y: e.evt.layerY });
    // button == 0 means left click
    if (e.evt.button === 0) {
      setBlocks(
        blocks.map((b) => ({
          ...b,
          isSelected: false,
        }))
      );
      setIsSmallMenuVisible(false);
      // button == 2 means right click
    } else if (e.evt.button === 2) {
      setIsSmallMenuVisible(true);
    }
  }

  function handleDefaultContextMenu(e: any) {
    e.evt.preventDefault();
  }

  return (
    <span>
      <Stage
        width={window.innerWidth}
        height={window.innerHeight}
        draggable={true}
        onClick={(e) => {
          handleClick(e);
        }}
        onContextMenu={(e) => {
          handleDefaultContextMenu(e);
        }}
        className={styles.mainStage}
      >
        <FlowLayer
          blocks={blocks}
          setBlocks={setBlocks}
          links={links}
          setLinks={setLinks}
          setSelectedLink={setSelectedLink}
          setIsLinkModalCreateVisible={setIsLinkModalCreateVisible}
          handleBlockDoubleClick={(block) => handleBlockDoubleClick(block)}
          handleLinkDoubleClick={(link) => handleLinkDoubleClick(link)}
        />
      </Stage>
      <SmallMenu
        show={isSmallMenuVisible}
        position_x={lastClickPosition.x}
        position_y={lastClickPosition.y}
        blocks={blocks}
        setBlocks={setBlocks}
      />
    </span>
  );
};

export default MainStage;
