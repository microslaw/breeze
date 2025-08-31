import { Rect, Text, Group, Circle } from "react-konva";
import { BlockI } from "../models/block.model";
import { useState } from "react";
import {
  handleBlockSingleClick,
  handleDragBlockEnd,
  handleDragBlockStart,
  handleDragCircleEnd,
  handleDragCircleStart,
  handleMouseEnter,
  handleMouseLeave,
} from "../functions/handleDefaultShapeInteractions";
import { LinkI } from "../models/link.model";
import Link from "./Link";
import LinkCircleI from "../models/linkcircle.model";
import { BLOCK_HEIGHT, BLOCK_WIDTH } from "../constants/ui";

interface BlockProps {
  block: BlockI;
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
  links: LinkI[];
  setLinks: React.Dispatch<React.SetStateAction<LinkI[]>>;
  setSelectedLink: React.Dispatch<React.SetStateAction<LinkI>>;
  setIsLinkModalCreateVisible: React.Dispatch<React.SetStateAction<boolean>>;
  handleDoubleClick: (block: BlockI) => void;
}

const Block = ({
  block,
  blocks,
  setBlocks,
  links,
  setLinks,
  setSelectedLink,
  setIsLinkModalCreateVisible,
  handleDoubleClick,
}: BlockProps) => {
  const [dynamicPosition, setdynamicPosition] = useState({
    x: block.x,
    y: block.y,
  });

  const [linkCircle, setLinkCircle] = useState<LinkCircleI>({
    isDragging: false,
    x: block.x + BLOCK_WIDTH,
    y: block.y + BLOCK_HEIGHT / 2,
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
        width={BLOCK_WIDTH}
        height={BLOCK_HEIGHT}
        fill="lightblue"
        opacity={0.8}
        shadowColor="black"
        shadowBlur={10}
        shadowOpacity={0.6}
        draggable
        stroke={block.isSelected ? "red" : ""}
        shadowOffsetX={block.isDragging ? 10 : 5}
        shadowOffsetY={block.isDragging ? 10 : 5}
        scaleX={block.isDragging ? 1.2 : 1}
        scaleY={block.isDragging ? 1.2 : 1}
        onDragStart={() => handleDragBlockStart(block, blocks, setBlocks)}
        onDragEnd={(e) =>
          handleDragBlockEnd(e, block, blocks, setBlocks, links, setLinks)
        }
        onDragMove={handleDragMove}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={() => handleBlockSingleClick(block, setBlocks)}
        onDblClick={() => handleDoubleClick(block)}
      />
      <Text
        x={dynamicPosition.x}
        y={dynamicPosition.y}
        text={block.name}
        fontSize={16}
        fontStyle="bold"
        fill="black"
        offsetX={-BLOCK_WIDTH / 10}
        offsetY={-BLOCK_HEIGHT / 10}
      />
      {block.isSelected && (
        <Circle
          draggable
          x={dynamicPosition.x + BLOCK_WIDTH}
          y={dynamicPosition.y + BLOCK_HEIGHT / 2}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          onDragStart={() => handleDragCircleStart(setLinkCircle)}
          onDragEnd={(e) => {
            handleDragCircleEnd(
              e,
              setLinkCircle,
              block,
              blocks,
              setBlocks,
              links,
              setLinks,
              setSelectedLink,
              setIsLinkModalCreateVisible
            );
          }}
          radius={linkCircle.isDragging ? 14 : 10}
          fill="red"
          stroke={"black"}
        />
      )}
    </Group>
  );
};

export default Block;
