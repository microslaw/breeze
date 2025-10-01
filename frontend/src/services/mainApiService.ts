import axios from "axios";
import {
  mapApiResponseToBlocks,
  mapBlockToApiPostRequest,
  mapPartialBlockToApiPatchRequest,
} from "../functions/apiMappers/blockApiMapper";
import { BlockI, PartialBlockI } from "../models/block.model";
import { LinkI } from "../models/link.model";
import {
  mapApiResponseToLinks,
  mapLinkToApiPostRequest,
} from "../functions/apiMappers/linkApiMapper";
import { ColourI } from "../models/colour.model";
import { NodeTypeI } from "../models/nodetype.model";
import { getNodeTypeColour } from "../functions/getBlockColourForNodeTypes";

// TODO assign response types to the functions
export async function getAllNodes(): Promise<BlockI[]> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/nodeInstances",
    });

    if (!Array.isArray(response.data)) {
      throw new Error("API response is not an array");
    }

    let blocks: BlockI[] = mapApiResponseToBlocks(response.data);

    return await enrichNodesByColour(blocks);
  } catch (error: any) {
    console.error("Error fetching nodes:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error fetching nodes: " + error);
    }
    throw error;
  }
}

export async function deleteNodeById(id: number) {
  try {
    const response = await axios({
      method: "delete",
      url: "http://127.0.0.1:5000/nodeInstances/" + id,
    });
    return response.data;
  } catch (error: any) {
    console.error("Error deleting node:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error deleting node: " + error);
    }
    throw error;
  }
}

export async function createNode(block: BlockI): Promise<{ node_id: number }> {
  const node = mapBlockToApiPostRequest(block);
  try {
    const response = await axios({
      method: "post",
      url: "http://127.0.0.1:5000/nodeInstances",
      headers: {
        "Content-Type": "application/json",
      },
      data: node,
    });
    return response.data;
  } catch (error: any) {
    console.error("Error creating node:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error creating node: " + error);
    }
    throw error;
  }
}

export async function updateNode(block: PartialBlockI) {
  const node = mapPartialBlockToApiPatchRequest(block);
  try {
    const response = await axios({
      method: "patch",
      url: "http://127.0.0.1:5000/nodeInstances/" + node.id,
      headers: {
        "Content-Type": "application/json",
      },
      data: node.attributes,
    });
    return response.data;
  } catch (error: any) {
    console.error("Error updating node:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error updating node: " + error);
    }
    throw error;
  }
}

// TODO implement non primitive handling of the response
export async function getNodeById(id: number) {
  const response = await axios({
    method: "get",
    url: "http://127.0.0.1:5000/nodeInstances/" + id,
  });
  return response.data;
}

export async function getAllLinks(): Promise<LinkI[]> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/nodeLinks",
    });

    if (!Array.isArray(response.data)) {
      throw new Error("API response is not an array");
    }

    const links: LinkI[] = mapApiResponseToLinks(response.data);
    return links;
  } catch (error: any) {
    console.error("Error fetching links:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error fetching links: " + error);
    }
    throw error;
  }
}

export async function deleteLinkById(id: number) {
  try {
    const response = await axios({
      method: "delete",
      url: "http://127.0.0.1:5000/nodeLinks/" + id,
    });
    return response.data;
  } catch (error: any) {
    console.error("Error deleting link:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error deleting link: " + error);
    }
    throw error;
  }
}

// TODO implement non primitive handling of the response
export async function getLinksByOriginNode(nodeId: number) {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/nodeLinks/" + nodeId,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching links by origin node:", error);
    alert("Error fetching links by origin node: " + error);
    throw error;
  }
}

// TODO implement non primitive handling of the response
// TODO add function to map LinkI to data send to backend
// for now we assume that node can have only one output
export async function createLink(link: LinkI) {
  const data = mapLinkToApiPostRequest(link);
  await axios({
    method: "post",
    url: "http://127.0.0.1:5000/nodeLinks",
    headers: {
      "Content-Type": "application/json",
    },
    data: data,
  })
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      console.error("Error creating link:", error);
      alert("Error creating link: " + error);
    });
}

// TODO implement non primitive handling of the response
export async function getNodeTypes(): Promise<NodeTypeI[]> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/nodeTypes",
    });

    if (!Array.isArray(response.data)) {
      throw new Error("API response is not an array");
    }

    return response.data;
  } catch (error: any) {
    console.error("Error fetching node types:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error fetching node types: " + error);
    }
    throw error;
  }
}

export async function getNodeTypesColourMap(): Promise<ColourI[]> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/nodeTypes/colours",
    });

    const data = response.data;

    // map object from api to colours array
    // TODO move to separate function
    const colourMap: ColourI[] = Object.entries(data).map(([tag, colour]) => ({
      tag: tag,
      colour: colour as string,
    }));
    return colourMap;
  } catch (error: any) {
    console.error("Error fetching node types colour map:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error fetching node type colour map: " + error);
    }
    throw error;
  }
}

export async function enrichNodesByColour(blocks: BlockI[]): Promise<BlockI[]> {
  const blocksEnriched = getNodeTypesColourMap()
    .then(async (colourMap) => {
      const nodeTypes = await getNodeTypes();
      blocks.forEach((block) => {
        const nodeTypeFull = nodeTypes.find((t) => t.name === block.type);

        if (nodeTypeFull) {
          block.colour = getNodeTypeColour(nodeTypeFull, colourMap);
        }
      });
      return blocks;
    })
    .catch((error: any) => {
      console.error("Error fetching node type colour map:", error);
      if (error.response && error.response.status === 500) {
        alert("can not connect with the server");
      } else {
        alert("Error fetching node type colour map: " + error);
      }
      throw error;
    });
  return blocksEnriched;
}

export async function getNodeTypesEnrichedByColour(): Promise<NodeTypeI[]> {
  const nodeTypesEnriched = await getNodeTypesColourMap().then(
    async (colourMap) => {
      const nodeTypes = await getNodeTypes();
      nodeTypes.forEach((nodeType) => {
        nodeType.colour = getNodeTypeColour(nodeType, colourMap);
      });
      return nodeTypes;
    }
  );
  return nodeTypesEnriched;
}
