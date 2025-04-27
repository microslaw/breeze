import React from "react";
import { Arrow } from "react-konva";
import { LinkI } from "../models/link.model";

interface LinkProps {
  link: LinkI;
  color?: string;
  strokeWidth?: number;
}

const Link: React.FC<LinkProps> = ({ link }) => {
  return (
    <Arrow
      draggable
      points={[0, 0, 100, 100]}
      stroke="black"
      fill="black"
      strokeWidth={2}
      pointerLength={10}
      pointerWidth={10}
    />
  );
};

export default Link;
