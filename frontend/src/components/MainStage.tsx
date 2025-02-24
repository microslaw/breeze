import React from "react";
import { Stage } from "react-konva";
import FlowLayer from "./FlowLayer";
import { BlockI } from "../models/block.model";

interface MainStageProps {
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
}

const MainStage = ({ blocks, setBlocks }: MainStageProps) => {
  return (
    <Stage
      width={window.innerWidth}
      height={window.innerHeight}
      draggable={true}
    >
      <FlowLayer blocks={blocks} setBlocks={setBlocks} />
    </Stage>
  );
};

export default MainStage;
