import { Rect, Text, Group, Circle } from "react-konva";
import { BlockI } from "../models/block.model";
import { useState } from "react";
import {
  handleMouseEnter,
  handleMouseLeave,
} from "../functions/handleDefaultShapeInteractions";

interface BlockProps {
  block: BlockI;
  onDragBlockStart: (e: any) => void;
  onDragBlockEnd: (e: any) => void;
  onClick: (e: any) => void;
  handleDoubleClick: (block: BlockI) => void;
}
const RECTANGLE_WIDTH = 200;
const RECTANGLE_HEIGHT = 130;

const Block = ({
  block,
  onDragBlockStart,
  onDragBlockEnd,
  onClick,
  handleDoubleClick,
}: BlockProps) => {
  const [dynamicPosition, setdynamicPosition] = useState({
    x: block.x,
    y: block.y,
  });

  const handleDragMove = (e: any) => {
    setdynamicPosition({ x: e.target.x(), y: e.target.y() });
  };

  return (
    <Group>
      <Rect
        key={block.id}
        id={block.id.toString()}
        x={block.x}
        y={block.y}
        width={RECTANGLE_WIDTH}
        height={RECTANGLE_HEIGHT}
        fill="lightblue"
        opacity={0.8}
        shadowColor="black"
        shadowBlur={10}
        shadowOpacity={0.6}
        draggable={!block.isSelected}
        stroke={block.isSelected ? "red" : ""}
        shadowOffsetX={block.isDragging ? 10 : 5}
        shadowOffsetY={block.isDragging ? 10 : 5}
        scaleX={block.isDragging ? 1.2 : 1}
        scaleY={block.isDragging ? 1.2 : 1}
        onDragStart={onDragBlockStart}
        onDragEnd={onDragBlockEnd}
        onDragMove={handleDragMove}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={onClick}
        onDblClick={() => handleDoubleClick(block)}
      />
      <Text
        x={dynamicPosition.x}
        y={dynamicPosition.y}
        text={block.name}
        fontSize={16}
        fontStyle="bold"
        fill="black"
        offsetX={-RECTANGLE_WIDTH / 10}
        offsetY={-RECTANGLE_HEIGHT / 10}
      />
      {block.isSelected && (
        <Circle
          draggable
          x={dynamicPosition.x + RECTANGLE_WIDTH}
          y={dynamicPosition.y + RECTANGLE_HEIGHT / 2}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          radius={10}
          fill="red"
          stroke={"black"}
        />
      )}
    </Group>
  );
};

export default Block;
