import axios from "axios";
import { KwargI } from "../models/kwarg.model";

export async function updateKwargByNodeId(nodeId: number, kwarg: KwargI) {
  try {
    const response = await axios({
      method: "put",
      url:
        "http://127.0.0.1:5000/nodeInstances/" +
        nodeId +
        "/kwargs/" +
        kwarg.key,
      headers: {
        "Content-Type": "text/plain",
      },
      data: kwarg.value,
    });
    return response.data;
  } catch (error) {
    console.error("Error updating kwarg:", error);
    throw error;
  }
}
