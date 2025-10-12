import { BlockI } from "../models/block.model";
import { SSEMessageI, SSEMessageType } from "../models/ssemessage.model";

export async function startSSE(
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>,
  processingQueue: number[],
  setProcessingQueue: React.Dispatch<React.SetStateAction<number[]>>
) {
  const es = new EventSource("http://127.0.0.1:5000/stream");
  es.onopen = (e) => console.log("Connection opened!", e);
  es.onerror = (e) => console.log("ERROR!", e);
  es.onmessage = (e) => {
    const data: SSEMessageI = JSON.parse(e.data.replace(/'/g, '"'));
    console.log(data);
    handleMessageByType(
      data,
      blocks,
      setBlocks,
      processingQueue,
      setProcessingQueue
    );
  };

  return () => es.close();
}

function handleMessageByType(
  message: SSEMessageI,
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>,
  processingQueue: number[],
  setProcessingQueue: React.Dispatch<React.SetStateAction<number[]>>
) {
  switch (message.type) {
    case SSEMessageType.FinishedProcessing: {
      handleMessageTypeFinishedProcessing(
        message,
        blocks,
        setBlocks,
        processingQueue,
        setProcessingQueue
      );
      break;
    }
    default:
      console.log("Unknown message type:", message.type);
      break;
  }
}

function handleMessageTypeFinishedProcessing(
  message: SSEMessageI,
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>,
  processingQueue: number[],
  setProcessingQueue: React.Dispatch<React.SetStateAction<number[]>>
) {
  const { node_id, processing_queue } = message.content;

  console.log("Finished processing node id:", node_id);
  setBlocks((prevBlocks) => {
    const updatedBlocks = [...prevBlocks];
    updatedBlocks.forEach((block) => {
      if (block.id === node_id) {
        console.log("Updating block id:", block.id);
        block.isQueued = false;
        block.isProcessed = true;
      }
    });
    return updatedBlocks;
  });

  setProcessingQueue(processing_queue);
}
