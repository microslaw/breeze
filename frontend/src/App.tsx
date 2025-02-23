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

function App() {
  const INITIAL_STATE: BlockI[] = generateShapes();
  const [blocks, setBlocks] = React.useState<BlockI[]>(INITIAL_STATE);

  const handleDragStart = (e: any, items: any[], setItems: React.Dispatch<React.SetStateAction<any[]>>) => {
    const id = e.target.id();
    setItems(
      items.map((element) => ({
        ...element,
        isDragging: element.id === id,
      }))
    );
  };

  const handleDragEnd = (e: any, items: any[], setItems: React.Dispatch<React.SetStateAction<any[]>>) => {
    setItems(
      items.map((element) => {
        if (element.id === e.target.id()) {
          return {
            ...element,
            x: e.target.x(),
            y: e.target.y(),
            isDragging: false,
          };
        }
        return element;
      })
    );
  };

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
