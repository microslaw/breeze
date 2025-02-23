import React from "react";
import { Rect } from "react-konva";
import { BlockI} from "../models/block.model";

interface BlockProps {
  block: BlockI;
  onDragStart: (e: any) => void;
  onDragEnd: (e: any) => void;
}

const Block = ({ block, onDragStart, onDragEnd }: BlockProps) => {    
    return (
        <Rect
        key={block.id}
        id={block.id}
        x={block.x}
        y={block.y}
        width={50}
        height={50}
        fill="blue"
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
        />
    );
};

export default Block;
