import { BlockI } from "../../models/block.model";

export function mapApiResponseToBlocks(apiResponse: any[]): BlockI[] {
  console.log("Mapping API response to blocks:", apiResponse);
  return apiResponse.map((node) => ({
    name: node.node_type,
    type: node.node_type,
    id: node.node_id,
    x: node.position_x,
    y: node.position_y,
    isDragging: false,
  }));
}

export function mapBlockToApiPostRequest(block: BlockI): any {
  return {
    node_type: block.type,
    position_x: block.x,
    position_y: block.y,
  };
}
