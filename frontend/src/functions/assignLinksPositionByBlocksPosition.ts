import { BlockI } from "../models/block.model";
import { LinkI } from "../models/link.model";

export default function assignLinksPositionByBlocksPosition(
  blocks: BlockI[],
  links: LinkI[]
): void {
  links.forEach((link) => {
    const sourceBlock = blocks.find((block) => block.id === link.originNodeId);
    const targetBlock = blocks.find(
      (block) => block.id === link.destinationNodeId
    );
    if (sourceBlock && targetBlock) {
      link.startX = sourceBlock.x + 200;
      link.startY = sourceBlock.y + 65;
      link.endX = targetBlock.x;
      link.endY = targetBlock.y + 65;
    } else {
      console.log(
        sourceBlock,
        targetBlock,
        "sourceBlock or targetBlock not found"
      );
    }
  });
}
