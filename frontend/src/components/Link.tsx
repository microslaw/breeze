import React, { useRef, useEffect } from "react";
import { Arrow, Circle, Group, Text } from "react-konva";
import { LinkI } from "../models/link.model";
import {
  handleMouseEnter,
  handleMouseLeave,
} from "../functions/handleDefaultShapeInteractions";
import getLinkEndLabelPosition from "../functions/getLinkEndLabelPosition";

interface LinkProps {
  link: LinkI;
  handleDoubleClick: (link: LinkI) => void;
  pointerSize?: number;
  onDragStart?: (e: any) => void;
  onDragEnd?: (e: any) => void;
  onDragMove?: (e: any) => void;
  draggable?: boolean;
}

const Link = ({
  link,
  handleDoubleClick,
  pointerSize,
  onDragStart,
  onDragEnd,
  onDragMove,
  draggable,
}: LinkProps) => {
  const labelPos = getLinkEndLabelPosition(
    link.startX,
    link.startY,
    link.endX,
    link.endY
  );
  return (
    <Group>
      <Arrow
        draggable={draggable || false}
        points={[link.startX, link.startY, link.endX, link.endY]}
        stroke="darkSlateGray"
        fill="darkSlateGray"
        strokeWidth={2}
        pointerLength={pointerSize || 10}
        pointerWidth={pointerSize || 10}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onDblClick={() => handleDoubleClick(link)}
        onDragStart={onDragStart}
        onDragEnd={onDragEnd}
        onDragMove={onDragMove}
      />
      <Text
        text={link.destinationNodeInput}
        x={labelPos.x}
        y={labelPos.y}
        fontSize={14}
        fontStyle="bold"
        fill={"#232323ff"}
        stroke={"#bebebeff"}
        strokeWidth={0.1}
      />
    </Group>
  );
};

export default Link;
