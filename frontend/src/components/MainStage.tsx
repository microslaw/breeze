import React, { useRef, useState } from "react";
import { Stage } from "react-konva";
import FlowLayer from "./FlowLayer";
import { BlockI } from "../models/block.model";
import { LinkI } from "../models/link.model";
import styles from "./MainStage.module.css";
import SmallMenu from "./SmallMenu";
import ZoomButtons from "./ZoomButtons";
import { handleWheel } from "./../functions/mainStageActions";

interface MainStageProps {
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
  links: LinkI[];
  setLinks: React.Dispatch<React.SetStateAction<LinkI[]>>;
  setSelectedLink: React.Dispatch<React.SetStateAction<LinkI>>;
  setIsBlockModalCreateVisible: React.Dispatch<React.SetStateAction<boolean>>;
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
  setIsBlockModalCreateVisible,
  setIsLinkModalCreateVisible,
  handleBlockDoubleClick,
  handleLinkDoubleClick,
}: MainStageProps) => {
  const width = window.innerWidth;
  const height = window.innerHeight;

  const [isSmallMenuVisible, setIsSmallMenuVisible] = useState<boolean>(false);
  const [lastClickPosition, setLastClickPosition] = useState<{
    x: number;
    y: number;
  }>({ x: 0, y: 0 });

  const stageRef = useRef(null);

  function handleClick(e: any) {
    setLastClickPosition({ x: e.evt.layerX, y: e.evt.layerY });

    // button == 0 means left click
    if (e.evt.button === 0) {
      handleLeftClick(e);
      // button == 2 means right click
    } else if (e.evt.button === 2) {
      handleRightClick(e);
    }
  }

  function handleLeftClick(e: any) {
    setIsSmallMenuVisible(false);

    if (e.target === e.target.getStage()) {
      setBlocks(
        blocks.map((b) => ({
          ...b,
          isSelected: false,
        }))
      );
    }
  }

  function handleRightClick(e: any) {
    e.evt.preventDefault();
    if (e.target === e.target.getStage()) {
      setIsSmallMenuVisible(true);
    }
  }

  function handleDefaultContextMenu(e: any) {
    e.evt.preventDefault();
  }

  return (
    <span>
      <Stage
        width={width}
        height={height}
        draggable={true}
        onClick={(e) => {
          handleClick(e);
        }}
        onContextMenu={(e) => {
          handleDefaultContextMenu(e);
        }}
        className={styles.mainStage}
        ref={stageRef}
        onWheel={(e) => handleWheel(e, stageRef)}
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
        setShow={setIsSmallMenuVisible}
        position_x={lastClickPosition.x}
        position_y={lastClickPosition.y}
        setIsBlockModalCreateVisible={setIsBlockModalCreateVisible}
      />
      <ZoomButtons stage={stageRef.current}></ZoomButtons>
    </span>
  );
};

export default MainStage;
