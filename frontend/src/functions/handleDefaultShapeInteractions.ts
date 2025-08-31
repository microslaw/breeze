import { BLOCK_HEIGHT, BLOCK_WIDTH } from "../constants/ui";
import { BlockI } from "../models/block.model";
import { LinkI } from "../models/link.model";
import LinkCircleI from "../models/linkcircle.model";
import {
  createLink,
  getAllLinks,
  updateNode,
} from "../services/mainApiService";
import { mapBlockToPartialBlockForApiPatchRequestPositionUpdate } from "./apiMappers/blockApiMapper";
import assignLinksPositionByBlocksPosition from "./assignLinksPositionByBlocksPosition";

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
        link.startX = e.target.x() + BLOCK_WIDTH;
        link.startY = e.target.y() + BLOCK_HEIGHT / 2;
      }
      if (link.destinationNodeId === block.id) {
        link.endX = e.target.x();
        link.endY = e.target.y() + BLOCK_HEIGHT / 2;
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
  setLinkCircle((prev: LinkCircleI) => ({ ...prev, isDragging: true }));
};

export const handleDragCircleEnd = (
  e: any,
  setLinkCircle: React.Dispatch<React.SetStateAction<LinkCircleI>>,
  block: BlockI,
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>,
  links: LinkI[],
  setLinks: React.Dispatch<React.SetStateAction<LinkI[]>>,
  setSelectedLink: React.Dispatch<React.SetStateAction<LinkI>>,
  setIsLinkModalCreateVisible: React.Dispatch<React.SetStateAction<boolean>>
) => {
  setLinkCircle((prev: LinkCircleI) => ({ ...prev, isDragging: false }));

  const circleX = e.target.x();
  const circleY = e.target.y();
  const circleRadius = e.target.radius();

  blocks.forEach((destBlock) => {
    const isOverlapping =
      circleX + circleRadius > destBlock.x &&
      circleX - circleRadius < destBlock.x + BLOCK_WIDTH &&
      circleY + circleRadius > destBlock.y &&
      circleY - circleRadius < destBlock.y + BLOCK_HEIGHT;

    if (isOverlapping) {
      const newLink = {
        id: -1,
        originNodeId: block.id,
        originNodeOutput: "",
        destinationNodeId: destBlock.id,
        destinationNodeInput: "",
        startX: 0,
        startY: 0,
        endX: 0,
        endY: 0,
      };
      if (!validateLink(newLink, links)) {
        return;
      }

      setSelectedLink(newLink);
      setIsLinkModalCreateVisible(true);
    }

    setBlocks((prevBlocks) =>
      prevBlocks.map((b) => ({
        ...b,
        isSelected: false,
      }))
    );
  });
};

function validateLink(link: LinkI, links: LinkI[]): boolean {
  const isValid =
    link.originNodeId !== link.destinationNodeId &&
    !links.some(
      (existingLink) =>
        existingLink.originNodeId === link.originNodeId &&
        existingLink.destinationNodeId === link.destinationNodeId
    );
  return isValid;
}
