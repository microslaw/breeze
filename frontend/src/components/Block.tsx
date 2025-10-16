import { Rect, Text, Group, Circle } from "react-konva";
import { BlockI } from "../models/block.model";
import { useState } from "react";
import {
  handleBlockDragMove,
  handleBlockSingleClick,
  handleDragBlockEnd,
  handleDragBlockStart,
  handleDragCircleEnd,
  handleDragCircleStart,
  handleMouseEnter,
  handleMouseLeave,
} from "../functions/handleDefaultShapeInteractions";
import { LinkI } from "../models/link.model";
import LinkCircleI from "../models/linkcircle.model";
import { BLOCK_HEIGHT, BLOCK_WIDTH } from "../constants/ui";
import Loader from "./Loader";
import RunJobShape from "./RunJobShape";

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
const BLOCK_SCALE_WHEN_DRAGGING = 1.15;

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
  const [dynamicPosition, setDynamicPosition] = useState({
    x: block.x,
    y: block.y,
  });

  const [linkCircle, setLinkCircle] = useState<LinkCircleI>({
    isDragging: false,
    x: block.x + BLOCK_WIDTH,
    y: block.y + BLOCK_HEIGHT / 2,
  });

  return (
    <Group>
      <Rect
        perfectDrawEnabled={false}
        key={block.id}
        id={block.id.toString()}
        x={block.x}
        y={block.y}
        width={BLOCK_WIDTH}
        height={BLOCK_HEIGHT}
        fill={block.colour}
        opacity={0.8}
        shadowColor="black"
        shadowBlur={10}
        shadowOpacity={0.6}
        draggable
        stroke={block.isSelected ? "lightSlateGray" : ""}
        shadowOffsetX={block.isDragging ? 5 : 2.5}
        shadowOffsetY={block.isDragging ? 5 : 2.5}
        scaleX={block.isDragging ? BLOCK_SCALE_WHEN_DRAGGING : 1}
        scaleY={block.isDragging ? BLOCK_SCALE_WHEN_DRAGGING : 1}
        onDragStart={() => handleDragBlockStart(block, blocks, setBlocks)}
        onDragEnd={(e) =>
          handleDragBlockEnd(e, block, blocks, setBlocks, links, setLinks)
        }
        onDragMove={(e) =>
          handleBlockDragMove(
            e,
            block,
            setLinks,
            setDynamicPosition,
            BLOCK_SCALE_WHEN_DRAGGING
          )
        }
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={() => handleBlockSingleClick(block, setBlocks)}
        onDblClick={() => handleDoubleClick(block)}
      />
      <Loader
        show={block.isQueued && !block.isProcessed}
        x={dynamicPosition.x + (BLOCK_WIDTH * 8.5) / 10}
        y={dynamicPosition.y + (BLOCK_HEIGHT * 2.5) / 10}
      />
      <RunJobShape
        show={!block.isQueued && !block.isProcessed}
        x={dynamicPosition.x + (BLOCK_WIDTH * 8.5) / 10}
        y={dynamicPosition.y + (BLOCK_HEIGHT * 2.5) / 10}
        id={block.id}
      ></RunJobShape>
      {block.isProcessed && (
        <Text
          text={"\u2713"}
          fontSize={28}
          fontStyle="bold"
          stroke="black"
          strokeWidth={0.3}
          fill="#197148ff"
          x={dynamicPosition.x + (BLOCK_WIDTH * 7.25) / 10}
          y={dynamicPosition.y + (BLOCK_HEIGHT * 1.25) / 10}
        />
      )}
      <Text
        x={dynamicPosition.x}
        y={dynamicPosition.y}
        text={block.name.replaceAll("_", " ")}
        fontSize={10}
        fontStyle="bold"
        fill={"#232323ff"}
        width={BLOCK_WIDTH - (BLOCK_WIDTH * 4) / 10}
        offsetX={-BLOCK_WIDTH / 10}
        offsetY={-BLOCK_HEIGHT / 8}
      />
      <Text
        x={dynamicPosition.x}
        y={dynamicPosition.y}
        text={block.id.toString()}
        fontSize={30}
        fontStyle="bold"
        fill={block.colour}
        stroke="black"
        strokeWidth={0.3}
        offsetX={-BLOCK_WIDTH * 0.1}
        offsetY={-BLOCK_HEIGHT * 0.55}
      ></Text>
      {block.isSelected && (
        <Circle
          perfectDrawEnabled={false}
          draggable
          x={
            dynamicPosition.x +
            BLOCK_WIDTH * (block.isDragging ? BLOCK_SCALE_WHEN_DRAGGING : 1)
          }
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
          radius={linkCircle.isDragging ? 7 : 5}
          fill="darkSlateGray"
          stroke={"lightSlateGray"}
        />
      )}
    </Group>
  );
};

export default Block;
