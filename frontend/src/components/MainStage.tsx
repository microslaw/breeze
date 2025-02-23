import React from "react";
import { Stage } from "react-konva";
import FlowLayer from "./FlowLayer";

const MainStage: React.FC = () => {
  return (
    <Stage width={window.innerWidth} height={window.innerHeight}>
      <FlowLayer />
    </Stage>
  );
};

export default MainStage;
