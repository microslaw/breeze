import React from "react";
import { Layer } from "react-konva";
import Block from "./Block";
import { BlockI } from "../models/block.model";
import {
  handleDragBlockStart,
  handleDragBlockEnd,
} from "../functions/handleDefaultShapeInteractions";
import { LinkI } from "../models/link.model";
import Link from "./Link";

interface FlowLayerProps {
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
  links: LinkI[];
  setLinks: React.Dispatch<React.SetStateAction<LinkI[]>>;
  handleBlockDoubleClick: (block: BlockI) => void;
  handleLinkDoubleClick: (link: LinkI) => void;
}

const FlowLayer = ({
  blocks,
  setBlocks,
  links,
  setLinks,
  handleBlockDoubleClick,
  handleLinkDoubleClick,
}: FlowLayerProps) => {
  return (
    <Layer>
      {blocks.map((block) => (
        <Block
          key={block.id}
          block={block}
          onDragStart={(e) => handleDragBlockStart(block, blocks, setBlocks)}
          onDragEnd={(e) =>
            handleDragBlockEnd(e, block, blocks, setBlocks, links, setLinks)
          }
          handleDoubleClick={(block) => handleBlockDoubleClick(block)}
        />
      ))}
      {links.map((link, index) => (
        <Link
          key={index}
          link={link}
          handleDoubleClick={handleLinkDoubleClick}
        />
      ))}
    </Layer>
  );
};

export default FlowLayer;
