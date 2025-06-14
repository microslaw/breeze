import { BlockI } from "../models/block.model";

// DEPRECATED: This function was only used for testing without backend integration.
// It is not used in the current version of the code.
export function generateShapes(): BlockI[] {
  return [...Array(3)].map((_, i) => ({
    name: `Block ${i}`,
    type: "test",
    id: Math.floor(Math.random() * 1000000),
    x: Math.floor(Math.random() * (window.innerWidth / 100)) * 100,
    y: Math.floor(Math.random() * (window.innerHeight / 100)) * 100,
    isDragging: false,
    kwargs: [],
  }));
}
