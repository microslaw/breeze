import { BlockI } from "../models/block.model";
import { LinkI } from "../models/link.model";
import { createLink, updateNode } from "../services/mainApiService";
import { mapBlockToPartialBlockForApiPatchRequestPositionUpdate } from "./apiMappers/blockApiMapper";

// Generic interactions
export const handleMouseEnter = (e: any) => {
  e.target.getStage().container().style.cursor = "pointer";
};

export const handleMouseLeave = (e: any) => {
  e.target.getStage().container().style.cursor = "default";
};

// Block interactions
export const handleDragBlockStart = (
  block: BlockI,
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<any[]>>
) => {
  if (block.isSelected) return;
  setBlocks(
    blocks.map((element) => ({
      ...element,
      isDragging: element.id === block.id,
    }))
  );
};

export const handleDragBlockEnd = (
  e: any,
  block: BlockI,
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<any[]>>,
  links: LinkI[],
  setLinks: React.Dispatch<React.SetStateAction<any[]>>
) => {
  setBlocks(
    blocks.map((element) => {
      if (element.id === block.id) {
        element.isDragging = false;
        element.x = e.target.x();
        element.y = e.target.y();
        updateNode(
          mapBlockToPartialBlockForApiPatchRequestPositionUpdate(element)
        );
      }
      return element;
    })
  );

  setLinks(
    links.map((link) => {
      if (link.originNodeId === block.id) {
        link.startX = e.target.x() + 200;
        link.startY = e.target.y() + 65;
      }
      if (link.destinationNodeId === block.id) {
        link.endX = e.target.x();
        link.endY = e.target.y() + 65;
      }
      return link;
    })
  );
};

export const handleBlockSingleClick = (
  block: BlockI,
  setBlocks: React.Dispatch<React.SetStateAction<any[]>>
) => {
  setBlocks((prevBlocks) =>
    prevBlocks.map((b) => ({
      ...b,
      isSelected: b.id === block.id ? !b.isSelected : false,
    }))
  );
};

/// Circle interactions
export const handleDragCircleStart = (
  setLinkCircle: React.Dispatch<React.SetStateAction<LinkCircleI>>
) => {
  setLinkCircle((prev) => ({ ...prev, isDragging: true }));
};

export const handleDragCircleEnd = (
  e: any,
  setLinkCircle: React.Dispatch<React.SetStateAction<LinkCircleI>>,
  block: BlockI,
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>
) => {
  setLinkCircle((prev) => ({ ...prev, isDragging: false }));

  const circleX = e.target.x();
  const circleY = e.target.y();
  const circleRadius = e.target.radius();

  blocks.forEach((originBlock) => {
    const blockWidth = 200;
    const blockHeight = 130;

    const isOverlapping =
      circleX + circleRadius > originBlock.x &&
      circleX - circleRadius < originBlock.x + blockWidth &&
      circleY + circleRadius > originBlock.y &&
      circleY - circleRadius < originBlock.y + blockHeight;

    if (isOverlapping) {
      createLink(block, originBlock).then((res) => {
        console.log("Link created:", res);
      });
    }

    setBlocks((prevBlocks) =>
      prevBlocks.map((b) => ({
        ...b,
        isSelected: false,
      }))
    );
  });
};
