import React from "react";
import { Stage } from "react-konva";
import FlowLayer from "./FlowLayer";
import { BlockI } from "../models/block.model";
import { LinkI } from "../models/link.model";
import styles from "./MainStage.module.css";

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
  function handleClick(e: any) {
    if (e.target !== e.target.getStage()) return;

    // button == 0 means left click
    if (e.evt.button === 0) {
      setBlocks(
        blocks.map((b) => ({
          ...b,
          isSelected: false,
        }))
      );
      // button == 0 means right click
    } else if (e.evt.button === 2) {
      // TODO implement action on right click
    }
  }

  function handleDefaultContextMenu(e: any) {
    e.evt.preventDefault();
  }

  return (
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
  );
};

export default MainStage;
