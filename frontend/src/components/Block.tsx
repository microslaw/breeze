import { Rect, Text, Group, Circle } from "react-konva";
import { BlockI } from "../models/block.model";
import { useState } from "react";
import {
  handleBlockSingleClick,
  handleDragBlockEnd,
  handleDragBlockStart,
  handleDragLinkEnd,
  handleDragLinkStart,
  handleMouseEnter,
  handleMouseLeave,
} from "../functions/handleDefaultShapeInteractions";
import { LinkI } from "../models/link.model";
import Link from "./Link";

interface BlockProps {
  block: BlockI;
  blocks: BlockI[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>;
  links: LinkI[];
  setLinks: React.Dispatch<React.SetStateAction<LinkI[]>>;
  handleDoubleClick: (block: BlockI) => void;
}
const RECTANGLE_WIDTH = 200;
const RECTANGLE_HEIGHT = 130;

const Block = ({
  block,
  blocks,
  setBlocks,
  links,
  setLinks,
  handleDoubleClick,
}: BlockProps) => {
  const [dynamicPosition, setdynamicPosition] = useState({
    x: block.x,
    y: block.y,
  });

  const [createdLink, setCreatedLink] = useState<LinkI>({
    destinationNodeId: -1,
    destinationNodeInput: "",
    originNodeId: block.id,
    originNodeOutput: "",
    startX: dynamicPosition.x + RECTANGLE_WIDTH,
    startY: dynamicPosition.y + RECTANGLE_HEIGHT / 2,
    endX: dynamicPosition.x + RECTANGLE_WIDTH + 5,
    endY: dynamicPosition.y + RECTANGLE_HEIGHT / 2,
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
        offsetX={-RECTANGLE_WIDTH / 10}
        offsetY={-RECTANGLE_HEIGHT / 10}
      />
      {block.isSelected && (
        <Link
          draggable={true}
          key={block.id + "-link"}
          link={createdLink}
          handleDoubleClick={function (link: LinkI): void {}}
          onDragStart={() => handleDragLinkStart(createdLink, setCreatedLink)}
          onDragEnd={() => handleDragLinkEnd(createdLink, setCreatedLink)}
          pointerSize={20}
        />
      )}
    </Group>
  );
};

export default Block;
