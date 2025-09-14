import { BLOCK_DEFAULT_COLOUR } from "../constants/ui";
import { ColourI } from "../models/colour.model";
import { NodeTypeI } from "../models/nodetype.model";

export function getNodeTypeColour(
  nodeType: NodeTypeI,
  colorMap: ColourI[]
): string {
  const colour = colorMap.find((colour) => {
    nodeType.tags.find((tag) => tag === colour.tag);
  })?.colour;
  return colour ?? BLOCK_DEFAULT_COLOUR;
}
