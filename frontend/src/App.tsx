import ListGroup from "./components/ListGroup";
import Alert from "./components/Alert";
import Button from "./components/Button";
import { useState } from "react";
import { Stage, Layer, Rect, Circle } from "react-konva";
import Menu from "./components/Menu";
import React from "react";
import { generateShapes } from "./functions/generateInitShapes";
import { Block } from "./models/block.model";

function App() {
  const INITIAL_STATE: Block[] = generateShapes();
  const [blocks, setBlocks] = React.useState<Block[]>(INITIAL_STATE);

  const handleDragStart = (e: any) => {
    const id = e.target.id();
    setBlocks(
      blocks.map((block) => ({
        ...block,
        isDragging: block.id === id,
      }))
    );
  };

  const handleDragEnd = (e: any) => {
    setBlocks(
      blocks.map((block) => {
        if (block.id === e.target.id()) {
          return {
            ...block,
            x: e.target.x(),
            y: e.target.y(),
            isDragging: false,
          };
        }
        return block;
      })
    );
  };

  return (
    <div>
      <Menu />
      <Stage width={window.innerWidth} height={window.innerHeight}>
        <Layer>
          {blocks.map((block) => (
            <Rect
              key={block.id}
              id={block.id}
              x={block.x}
              y={block.y}
              width={50}
              height={50}
              fill="red"
              opacity={0.8}
              draggable
              shadowColor="black"
              shadowBlur={10}
              shadowOpacity={0.6}
              shadowOffsetX={block.isDragging ? 10 : 5}
              shadowOffsetY={block.isDragging ? 10 : 5}
              scaleX={block.isDragging ? 1.2 : 1}
              scaleY={block.isDragging ? 1.2 : 1}
              onDragStart={handleDragStart}
              onDragEnd={handleDragEnd}
            />
          ))}
        </Layer>
      </Stage>
    </div>
  );
}

export default App;
