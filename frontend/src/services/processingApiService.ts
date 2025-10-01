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
  } catch (error: any) {
    console.error("Error fetching processing result:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error fetching processing result: " + error);
    }
    throw error;
  }
}

export async function getProcessingResultMetadataByNodeId(
  nodeId: number
): Promise<any> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/processingResult/" + nodeId + "/metadata",
    });

    return response.data;
  } catch (error: any) {
    console.error("Error fetching processing result metadata:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error fetching processing result metadata: " + error);
    }
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
  } catch (error: any) {
    console.error("Error running processing job:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error running processing job: " + error);
    }
    throw error;
  }
}

export async function getProcessingQueue(): Promise<number[]> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/queueProcessing",
    });
    return response.data;
  } catch (error: any) {
    console.error("Error fetching processing queue:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error fetching processing queue: " + error);
    }
    throw error;
  }
}

export async function processAllNodes(): Promise<any> {
  try {
    await axios({
      method: "post",
      url: "http://127.0.0.1:5000/queueProcessing/all",
    });
    return;
  } catch (error: any) {
    console.error("Error fetching processing queue:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error fetching processing queue: " + error);
    }
    throw error;
  }
}
