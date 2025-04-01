import React from "react";
import { Layer } from "react-konva";
import Block from "./Block";
import { BlockI } from "../models/block.model";
import {
  handleDragStart,
  handleDragEnd,
} from "../functions/handleDefaultShapeInteractions";

interface FlowLayerProps {
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
  handleBlockDoubleClick: (block: BlockI) => void;
}

const FlowLayer = ({
  blocks,
  setBlocks,
  handleBlockDoubleClick,
}: FlowLayerProps) => {
  return (
    <Layer>
      {blocks.map((block) => (
        <Block
          key={block.id}
          block={block}
          onDragStart={(e) => handleDragStart(e, blocks, setBlocks)}
          onDragEnd={(e) => handleDragEnd(e, blocks, setBlocks)}
          handleDoubleClick={(block) => handleBlockDoubleClick(block)}
        />
      ))}
    </Layer>
  );
};

export default FlowLayer;
