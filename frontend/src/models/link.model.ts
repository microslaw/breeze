// TODO add node_id to model
export interface LinkI {
  id: number;
  destinationNodeId: number;
  destinationNodeInput: string;
  originNodeId: number;
  originNodeOutput: string;
  startX: number;
  startY: number;
  endX: number;
  endY: number;
}
