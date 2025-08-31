import React, { useRef, useEffect } from "react";
import { Arrow } from "react-konva";
import { LinkI } from "../models/link.model";
import {
  handleMouseEnter,
  handleMouseLeave,
} from "../functions/handleDefaultShapeInteractions";

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
  return (
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
  );
};

export default Link;
