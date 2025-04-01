import { Rect, Text, Group } from "react-konva";
import { BlockI } from "../models/block.model";
import { useState } from "react";

interface BlockProps {
  block: BlockI;
  onDragStart: (e: any) => void;
  onDragEnd: (e: any) => void;
  handleDoubleClick: (block: BlockI) => void;
}
const RECTANGLE_WIDTH = 200;
const RECTANGLE_HEIGHT = 130;

const Block = ({
  block,
  onDragStart,
  onDragEnd,
  handleDoubleClick,
}: BlockProps) => {
  const [namePosition, setNamePosition] = useState({ x: block.x, y: block.y });

  const handleDragMove = (e: any) => {
    setNamePosition({ x: e.target.x(), y: e.target.y() });
  };

  const handleMouseEnter = (e: any) => {
    e.target.getStage().container().style.cursor = "pointer";
  };

  const handleMouseLeave = (e: any) => {
    e.target.getStage().container().style.cursor = "default";
  };

  return (
    <Group draggable>
      <Rect
        key={block.id}
        id={block.id}
        x={block.x}
        y={block.y}
        width={RECTANGLE_WIDTH}
        height={RECTANGLE_HEIGHT}
        fill="lightblue"
        opacity={0.8}
        draggable
        shadowColor="black"
        shadowBlur={10}
        shadowOpacity={0.6}
        shadowOffsetX={block.isDragging ? 10 : 5}
        shadowOffsetY={block.isDragging ? 10 : 5}
        scaleX={block.isDragging ? 1.2 : 1}
        scaleY={block.isDragging ? 1.2 : 1}
        onDragStart={onDragStart}
        onDragEnd={onDragEnd}
        onDragMove={handleDragMove}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onDblClick={() => handleDoubleClick(block)}
      />
      <Text
        x={namePosition.x}
        y={namePosition.y}
        text={block.name}
        fontSize={16}
        fontStyle="bold"
        fill="black"
        offsetX={-RECTANGLE_WIDTH / 10}
        offsetY={-RECTANGLE_HEIGHT / 10}
      />
    </Group>
  );
};

export default Block;
