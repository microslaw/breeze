import React from "react";
import { Arrow } from "react-konva";
import { LinkI } from "../models/link.model";
import {
  handleMouseEnter,
  handleMouseLeave,
} from "../functions/handleDefaultShapeInteractions";

interface LinkProps {
  link: LinkI;
  color?: string;
  strokeWidth?: number;
  handleDoubleClick: (link: LinkI) => void;
}

const Link: React.FC<LinkProps> = ({ link, handleDoubleClick }) => {
  return (
    <Arrow
      points={[link.startX, link.startY, link.endX, link.endY]}
      stroke="black"
      fill="black"
      strokeWidth={2}
      pointerLength={10}
      pointerWidth={10}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onDblClick={() => handleDoubleClick(link)}
    />
  );
};

export default Link;
