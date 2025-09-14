import { KwargI } from "./kwarg.model";

export interface BlockI {
  id: number;
  name: string;
  type: string;
  x: number;
  y: number;
  isDragging: boolean;
  // Used to indicate the mode which allows user to add links to other blocks
  isSelected: boolean;
  isQueued: boolean;
  kwargs: KwargI[];
  colour: string;
}

// Used only for updating the block using patch request
export interface PartialBlockI {
  id: number;
  name?: string;
  type?: string;
  x?: number;
  y?: number;
}
