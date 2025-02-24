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
}

const FlowLayer: React.FC<FlowLayerProps> = ({ blocks, setBlocks }) => {
  return (
    <Layer>
      {blocks.map((block) => (
        <Block
          key={block.id}
          block={block}
          onDragStart={(e) => handleDragStart(e, blocks, setBlocks)}
          onDragEnd={(e) => handleDragEnd(e, blocks, setBlocks)}
        />
      ))}
    </Layer>
  );
};

export default FlowLayer;
