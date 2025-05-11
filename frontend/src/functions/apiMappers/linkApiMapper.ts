import { LinkI } from "../../models/link.model";

export default function mapApiResponseToLinks(apiResponse: any[]): LinkI[] {
  console.log("Mapping API response to links:", apiResponse);
  // console.log("Mapping API response to links:", apiResponse);
  return apiResponse.map((link) => ({
    destinationNodeId: link.destination_node_id,
    destinationNodeInput: link.destination_node_input,
    originNodeId: link.origin_node_id,
    originNodeOutput: link.origin_node_output,
    startX: link.source_x || 0,
    startY: link.source_y || 0,
    endX: link.target_x || 0,
    endY: link.target_y || 100,
  }));
}
