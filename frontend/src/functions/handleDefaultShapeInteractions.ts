import { BlockI } from "../models/block.model";
import { LinkI } from "../models/link.model";
import { updateNode } from "../services/mainApiService";
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
  setItems: React.Dispatch<React.SetStateAction<any[]>>
) => {
  const id = block.id;
  setItems(
    blocks.map((element) => ({
      ...element,
      isDragging: element.id === id,
    }))
  );
};

export const handleDragBlockEnd = (
  e: any,
  block: BlockI,
  blocks: BlockI[],
  setItems: React.Dispatch<React.SetStateAction<any[]>>,
  links: LinkI[],
  setLinks: React.Dispatch<React.SetStateAction<any[]>>
) => {
  setItems(
    blocks.map((element) => {
      if (element.id === block.id) {
        element.isDragging = false;
        element.x = e.target.x();
        element.y = e.target.y();
        updateNode(
          mapBlockToPartialBlockForApiPatchRequestPositionUpdate(element)
        ).then((response) => {
          console.log("updated node position on backend", response);
        });
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
