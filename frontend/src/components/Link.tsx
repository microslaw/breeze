import React from "react";
import { Arrow } from "react-konva";
import { LinkI } from "../models/link.model";

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
      onDblClick={() => handleDoubleClick(link)}
    />
  );
};

export default Link;
