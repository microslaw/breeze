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
  handleBlockDoubleClick: (block: BlockI) => void;
  handleLinkDoubleClick: (link: LinkI) => void;
}

const MainStage = ({
  blocks,
  setBlocks,
  links,
  setLinks,
  handleBlockDoubleClick,
  handleLinkDoubleClick,
}: MainStageProps) => {
  return (
    <Stage
      width={window.innerWidth}
      height={window.innerHeight}
      draggable={true}
    >
      <FlowLayer
        blocks={blocks}
        setBlocks={setBlocks}
        links={links}
        setLinks={setLinks}
        handleBlockDoubleClick={(block) => handleBlockDoubleClick(block)}
        handleLinkDoubleClick={(link) => handleLinkDoubleClick(link)}
      />
    </Stage>
  );
};

export default MainStage;
