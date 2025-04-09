import { BlockI } from "../models/block.model";
import { v4 as uuidv4 } from "uuid";

export function generateShapes(): BlockI[] {
  return [...Array(3)].map((_, i) => ({
    name: `Block ${i}`,
    type: "test",
    id: uuidv4(),
    x: Math.floor(Math.random() * (window.innerWidth / 100)) * 100,
    y: Math.floor(Math.random() * (window.innerHeight / 100)) * 100,
    isDragging: false,
  }));
}
