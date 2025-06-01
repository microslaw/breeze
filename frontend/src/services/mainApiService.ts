import axios from "axios";
import {
  mapApiResponseToBlocks,
  mapBlockToApiPostRequest,
  mapPartialBlockToApiPatchRequest,
} from "../functions/apiMappers/blockApiMapper";
import { BlockI, PartialBlockI } from "../models/block.model";
import mapApiResponseToLinks from "../functions/apiMappers/linkApiMapper";
import { LinkI } from "../models/link.model";

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

    const blocks: BlockI[] = mapApiResponseToBlocks(response.data);
    return blocks;
  } catch (error) {
    console.error("Error fetching nodes:", error);
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
  } catch (error) {
    console.error("Error deleting node:", error);
    throw error;
  }
}

export async function createNode(block: BlockI) {
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
  } catch (error) {
    console.error("Error creating node:", error);
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
  } catch (error) {
    console.error("Error updating node:", error);
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
  } catch (error) {
    console.error("Error fetching links:", error);
    throw error;
  }
}

// TODO implement non primitive handling of the response
export async function getLinksByOriginNode(nodeId: number) {
  const response = await axios({
    method: "get",
    url: "http://127.0.0.1:5000/nodeLinks/" + nodeId,
  });
  return response.data;
}

// TODO implement non primitive handling of the response
export async function getNodeTypes(): Promise<string[]> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/nodeTypes",
    });

    if (!Array.isArray(response.data)) {
      throw new Error("API response is not an array");
    }

    return response.data;
  } catch (error) {
    console.error("Error fetching node types:", error);
    throw error;
  }
}
