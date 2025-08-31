import { BLOCK_WIDTH } from "../../constants/ui";
import { LinkI } from "../../models/link.model";

export function mapApiResponseToLinks(apiResponse: any[]): LinkI[] {
  return apiResponse.map((link) => ({
    id: link.node_link_id,
    destinationNodeId: link.destination_node_id,
    destinationNodeInput: link.destination_node_input,
    originNodeId: link.origin_node_id,
    originNodeOutput: link.origin_node_output,
    startX: link.source_x || 0,
    startY: link.source_y || 0,
    endX: link.target_x || 0,
    endY: link.target_y || BLOCK_WIDTH,
  }));
}

export function mapLinkToApiPostRequest(link: LinkI): any {
  return {
    origin_node_id: link.originNodeId.toString(),
    // TODO change to node output picked by user when backend ready
    origin_node_output: null,
    destination_node_id: link.destinationNodeId.toString(),
    destination_node_input: link.destinationNodeInput || null,
  };
}
