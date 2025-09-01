import { BLOCK_HEIGHT, BLOCK_WIDTH } from "../constants/ui";
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
      link.startX = sourceBlock.x + BLOCK_WIDTH;
      link.startY = sourceBlock.y + BLOCK_HEIGHT / 2;
      link.endX = targetBlock.x;
      link.endY = targetBlock.y + BLOCK_HEIGHT / 2;
    } else {
      throw new Error(`Source or target block not found for link: ${link}`);
    }
  });
}
