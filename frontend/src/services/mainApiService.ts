import axios from "axios";
import {
  mapApiResponseToBlocks,
  mapBlockToApiPostRequest,
} from "../functions/apiMappers/blockApiMapper";
import { BlockI } from "../models/block.model";

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
    console.log(response.request);
    return blocks;
  } catch (error) {
    console.error("Error fetching nodes:", error);
    throw error;
  }
}

export async function deleteNodeById(id: number) {
  const response = await axios({
    method: "delete",
    url: "http://127.0.0.1:5000/nodeInstances/" + id,
  });
  console.log(response.data);
  return response.data;
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

// TODO implement non primitive handling of the response
export async function getNodeById(id: number) {
  const response = await axios({
    method: "get",
    url: "http://127.0.0.1:5000/nodeInstances/" + id,
  });
  console.log(response.data);
  return response.data;
}

// TODO implement non primitive handling of the response
export async function getAllLinks() {
  const response = await axios({
    method: "get",
    url: "http://127.0.0.1:5000/nodeLinks",
  });
  console.log(response.data);
  return response.data;
}

// TODO implement non primitive handling of the response
export async function getLinksByOriginNode(nodeId: number) {
  const response = await axios({
    method: "get",
    url: "http://127.0.0.1:5000/nodeLinks/" + nodeId,
  });
  console.log(response.data);
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

    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching node types:", error);
    throw error;
  }
}
