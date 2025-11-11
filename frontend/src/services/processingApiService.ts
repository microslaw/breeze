import axios from "axios";
import { BlockI } from "../models/block.model";

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

// TODO unify ts type (processing_error) to cover both sse message and this api response
export async function getProcessingException(): Promise<any> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/processingResult/exception",
    });
    return response.data;
  } catch (error: any) {
    console.error("Error fetching processing result all:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error fetching processing exception: " + error);
    }
    throw error;
  }
}

export async function clearProcessingException(): Promise<any> {
  try {
    await axios({
      method: "delete",
      url: "http://127.0.0.1:5000/processingResult/exception",
    });
    return;
  } catch (error: any) {
    console.error("Error clearing processing exception:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error clearing processing exception: " + error);
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

export async function getProcessingResultAll(): Promise<number[]> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/processingResult/all",
    });
    return response.data;
  } catch (error: any) {
    console.error("Error fetching processing result all:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error fetching processing result all: " + error);
    }
    throw error;
  }
}

export async function deleteProcessingResultByNodeId(
  nodeId: number
): Promise<any> {
  try {
    const response = await axios({
      method: "delete",
      url: "http://127.0.0.1:5000/processingResult/" + nodeId,
    });

    return response.data;
  } catch (error: any) {
    console.error("Error deleting processing result:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error deleting processing result: " + error);
    }
    throw error;
  }
}

export async function deleteProcessingResultForAllNodes(): Promise<any> {
  try {
    await axios({
      method: "delete",
      url: "http://127.0.0.1:5000/processingResult/all",
    });
    return;
  } catch (error: any) {
    console.error("Error deleting processing result:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error deleting processing result: " + error);
    }
    throw error;
  }
}

export async function enrichNodesByIsProcessed(
  blocks: BlockI[]
): Promise<BlockI[]> {
  try {
    const processedIds = await getProcessingResultAll();
    const blocksEnriched: BlockI[] = blocks.map((block) => {
      block.isProcessed = processedIds.includes(block.id);
      return block;
    });
    return blocksEnriched;
  } catch (error: any) {
    console.error("Error fetching processing result all:", error);
    if (error.response && error.response.status === 500) {
      alert("can not connect with the server");
    } else {
      alert("Error fetching processing result all: " + error);
    }
    throw error;
  }
}
