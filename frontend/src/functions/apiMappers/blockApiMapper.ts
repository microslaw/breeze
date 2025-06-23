import { BlockI, PartialBlockI } from "../../models/block.model";

export function mapApiResponseToBlocks(apiResponse: any[]): BlockI[] {
  return apiResponse.map((node) => ({
    id: node.node_id,
    // Use instance_name if available, otherwise fallback to node_type
    name: node.instance_name || node.node_type,
    type: node.node_type,
    x: node.position_x,
    y: node.position_y,
    isDragging: false,
    kwargs: [],
  }));
}

export function mapBlockToApiPostRequest(block: BlockI): any {
  return {
    instance_name: block.name,
    node_type: block.type,
    position_x: block.x,
    position_y: block.y,
  };
}

export function mapBlockToPartialBlockForApiPatchRequestPositionUpdate(
  block: BlockI
): PartialBlockI {
  return {
    id: block.id,
    x: block.x,
    y: block.y,
  };
}

export function mapPartialBlockToApiPatchRequest(block: PartialBlockI): {
  id: number;
  attributes: any;
} {
  const patchRequest: any = {};
  if (block.type) patchRequest.node_type = block.type;
  if (block.x !== undefined) patchRequest.position_x = block.x;
  if (block.y !== undefined) patchRequest.position_y = block.y;
  if (block.name) patchRequest.instance_name = block.name;
  return { id: block.id, attributes: patchRequest };
}
