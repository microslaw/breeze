import { Block } from "../models/block.model";

export function generateShapes(): Block[]{
    return [...Array(10)].map((_, i) => ({
      id: i.toString(),
      x: Math.floor(Math.random() * (window.innerWidth / 100)) * 100,
      y: Math.floor(Math.random() * (window.innerHeight / 100)) * 100,
      isDragging: false,
    }));
  }