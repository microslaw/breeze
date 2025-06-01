export interface BlockI {
  id: number;
  name: string;
  type: string;
  x: number;
  y: number;
  isDragging: boolean;
}

// Used only for updating the block using patch request
export interface PartialBlockI {
  id: number;
  name?: string;
  type?: string;
  x?: number;
  y?: number;
}
