import React from "react";
import { Stage } from "react-konva";
import FlowLayer from "./FlowLayer";
import { BlockI } from "../models/block.model";
import { LinkI } from "../models/link.model";

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
    console.log("Stage clicked", e);
  }

  function handleRightClick(e: any) {
    e.evt.preventDefault();
    console.log("Stage right-clicked", e);
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
        handleRightClick(e);
      }}
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
