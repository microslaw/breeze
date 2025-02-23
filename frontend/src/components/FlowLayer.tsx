import React from "react";
import { Layer } from "react-konva";
import Block from "./Block";
import { BlockI } from "../models/block.model";
import { handleDragStart, handleDragEnd } from "../functions/handleDefaultShapeInteractions";
import { generateShapes } from "../functions/generateInitShapes";

const FlowLayer: React.FC = () => {
  const INITIAL_STATE: BlockI[] = generateShapes();
  const [blocks, setBlocks] = React.useState<BlockI[]>(INITIAL_STATE);

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