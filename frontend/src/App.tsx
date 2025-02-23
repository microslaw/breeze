import ListGroup from "./components/ListGroup";
import Alert from "./components/Alert";
import Button from "./components/Button";
import { useState } from "react";
import { Stage, Layer, Rect, Circle } from "react-konva";
import Menu from "./components/Menu";
import React from "react";
import { generateShapes } from "./functions/generateInitShapes";
import { BlockI } from "./models/block.model";
import Block from "./components/Block";
import { handleDragStart, handleDragEnd } from "./functions/handleDefaultShapeInteractions";

function App() {
  const INITIAL_STATE: BlockI[] = generateShapes();
  const [blocks, setBlocks] = React.useState<BlockI[]>(INITIAL_STATE);

  return (
    <div>
      <Menu />
      <Stage width={window.innerWidth} height={window.innerHeight}>
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
      </Stage>
    </div>
  );
}

export default App;
