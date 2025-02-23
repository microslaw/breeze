import ListGroup from "./components/ListGroup";
import Alert from "./components/Alert";
import Button from "./components/Button";
import { useState } from "react";
import { Stage, Layer, Rect, Circle } from "react-konva";
import Menu from "./components/Menu";
import React from "react";

function generateShapes() {
  return [...Array(10)].map((_, i) => ({
    id: i.toString(),
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    rotation: Math.random() * 180,
    isDragging: false,
  }));
}

function App() {
  const INITIAL_STATE = generateShapes();
  const [blocks, setBlocks] = React.useState(INITIAL_STATE);

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
          <Rect x={300} y={300} width={50} height={50} fill="red" />
          <Circle x={400} y={200} stroke="black" radius={50} />
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
              rotation={block.rotation}
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
