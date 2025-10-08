import React from "react";
import { Layer } from "react-konva";
import Block from "./Block";
import { BlockI } from "../models/block.model";
import { LinkI } from "../models/link.model";
import Link from "./Link";

interface FlowLayerProps {
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
  links: LinkI[];
  setLinks: React.Dispatch<React.SetStateAction<LinkI[]>>;
  setSelectedLink: React.Dispatch<React.SetStateAction<LinkI>>;
  setIsLinkModalCreateVisible: React.Dispatch<React.SetStateAction<boolean>>;
  handleBlockDoubleClick: (block: BlockI) => void;
  handleLinkDoubleClick: (link: LinkI) => void;
}

const FlowLayer = ({
  blocks,
  setBlocks,
  links,
  setLinks,
  setSelectedLink,
  setIsLinkModalCreateVisible,
  handleBlockDoubleClick,
  handleLinkDoubleClick,
}: FlowLayerProps) => {
  // TODO change the comunication with child block to do not duplicate same parameters
  return (
    <>
      <Layer>
        {blocks.map((block) => (
          <Block
            key={block.id}
            block={block}
            blocks={blocks}
            setBlocks={setBlocks}
            links={links}
            setLinks={setLinks}
            setSelectedLink={setSelectedLink}
            setIsLinkModalCreateVisible={setIsLinkModalCreateVisible}
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
    </>
  );
};

export default FlowLayer;
