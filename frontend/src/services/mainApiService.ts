import axios from "axios";
import { mapApiResponseToBlocks } from "../functions/apiMappers/blockApiMapper";
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
    console.log(blocks);
    return blocks;
  } catch (error) {
    console.error("Error fetching nodes:", error);
    throw error;
  }
}

// TODO implement non primitive handling of the response
export async function getNodeById(id: number) {
  const response = await axios({
    method: "get",
    url: "http://127.0.0.1:5000/nodeInstances/" + id,
    responseType: "stream",
  });
  console.log(response.data);
  return response.data;
}

// TODO implement non primitive handling of the response
export async function getAllLinks() {
  const response = await axios({
    method: "get",
    url: "http://127.0.0.1:5000/nodeLinks",
    responseType: "stream",
  });
  console.log(response.data);
  return response.data;
}

// TODO implement non primitive handling of the response
export async function getLinksByOriginNode(nodeId: number) {
  const response = await axios({
    method: "get",
    url: "http://127.0.0.1:5000/nodeLinks/" + nodeId,
    responseType: "stream",
  });
  console.log(response.data);
  return response.data;
}

// TODO implement non primitive handling of the response
export async function getNodeTypes() {
  const response = await axios({
    method: "get",
    url: "http://127.0.0.1:5000/nodeTypes",
    responseType: "stream",
  });
  console.log(response.data);
  return response.data;
}
