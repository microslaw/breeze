import { BlockI } from "../../models/block.model";

// TODO update mapping when backend is ready
export function mapApiResponseToBlocks(apiResponse: any[]): BlockI[] {
  console.log("Mapping API response to blocks:", apiResponse);
  return apiResponse.map((node) => ({
    name: node.node_type,
    type: node.node_type,
    id: node.node_id.toString(),
    x: 0,
    y: 0,
    isDragging: false,
  }));
}
