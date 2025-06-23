import axios from "axios";

export async function getProcessingResultByNodeId(
  nodeId: number
): Promise<any> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/processingResult/" + nodeId,
    });

    return response.data;
  } catch (error) {
    // TODO handle error after changing the backend (404 => 204 when no processing result)
    // console.log("Error fetching processing :", error);
    throw error;
  }
}

export async function runProcessingJob(nodeId: number): Promise<any> {
  try {
    const response = await axios({
      method: "post",
      url: "http://127.0.0.1:5000/queueProcessing",
      data: {
        node_id: nodeId,
      },
    });

    return response.data;
  } catch (error) {
    console.error("Error running processing job:", error);
    throw error;
  }
}

export async function getProcessingQueue(): Promise<any[]> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/queueProcessing",
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching processing queue:", error);
    throw error;
  }
}
