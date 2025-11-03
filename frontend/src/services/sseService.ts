import { BlockI } from "../models/block.model";
import {
  SSEFinishedProcessingContentI,
  SSEMessageI,
  SSEMessageType,
  SSEProcessingErrorContentI,
} from "../models/ssemessage.model";
import { getProcessingQueue } from "./processingApiService";

export async function startSSE(
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>,
  processingQueue: number[],
  setProcessingQueue: React.Dispatch<React.SetStateAction<number[]>>,
  selectedBlockRef: React.MutableRefObject<BlockI>,
  setSelectedBlock: React.Dispatch<React.SetStateAction<BlockI>>
) {
  const es = new EventSource("http://127.0.0.1:5000/stream");
  es.onopen = (e) => console.log("Connection opened!", e);
  es.onerror = (e) => console.error("ERROR!", e);
  es.onmessage = (e) => {
    const data: SSEMessageI = JSON.parse(e.data);
    console.log("SSE Message received:", data);
    handleMessageByType(
      data,
      blocks,
      setBlocks,
      processingQueue,
      setProcessingQueue,
      selectedBlockRef,
      setSelectedBlock
    );
  };

  return () => es.close();
}

function handleMessageByType(
  message: SSEMessageI,
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>,
  processingQueue: number[],
  setProcessingQueue: React.Dispatch<React.SetStateAction<number[]>>,
  selectedBlockRef: React.MutableRefObject<BlockI>,
  setSelectedBlock: React.Dispatch<React.SetStateAction<BlockI>>
) {
  switch (message.type) {
    case SSEMessageType.FinishedProcessing: {
      handleMessageTypeFinishedProcessing(
        message.content as SSEFinishedProcessingContentI,
        blocks,
        setBlocks,
        processingQueue,
        setProcessingQueue,
        selectedBlockRef,
        setSelectedBlock
      );
      break;
    }
    case SSEMessageType.ProcessingError: {
      const errorContent = message.content as SSEProcessingErrorContentI;
      handleMessageTypeProcessingError(
        errorContent,
        setBlocks,
        setProcessingQueue
      );
      break;
    }
    default:
      console.error("Unknown message type:", message.type);
      break;
  }
}

function handleMessageTypeFinishedProcessing(
  messageContent: SSEFinishedProcessingContentI,
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>,
  processingQueue: number[],
  setProcessingQueue: React.Dispatch<React.SetStateAction<number[]>>,
  selectedBlockRef: React.MutableRefObject<BlockI>,
  setSelectedBlock: React.Dispatch<React.SetStateAction<BlockI>>
) {
  const { node_id, processing_queue } = messageContent;

  setBlocks((prevBlocks) => {
    const updatedBlocks = [...prevBlocks];
    updatedBlocks.forEach((block) => {
      if (block.id === node_id) {
        block.isQueued = false;
        block.isProcessed = true;
      }
      if (processing_queue.includes(block.id)) {
        block.isQueued = true;
      }
      if (block.id === selectedBlockRef.current.id) {
        selectedBlockRef.current.isProcessed = block.isProcessed;
        setSelectedBlock(selectedBlockRef.current);
      }
    });
    return updatedBlocks;
  });

  setProcessingQueue(processing_queue);
}

function handleMessageTypeProcessingError(
  messageContent: SSEProcessingErrorContentI,
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>,
  setProcessingQueue: React.Dispatch<React.SetStateAction<number[]>>
) {
  getProcessingQueue().then((updatedQueue) => {
    setProcessingQueue(updatedQueue);
    setBlocks((prevBlocks) => {
      const updatedBlocks = [...prevBlocks];
      updatedBlocks.forEach((block) => {
        updatedQueue.find((item) => block.id === item)
          ? (block.isQueued = true)
          : (block.isQueued = false);
      });
      return updatedBlocks;
    });
  });
  alert(
    "Processing error in node " +
      messageContent.origin.node_id +
      ". Check node details (or console) for more information."
  );
  console.error("Processing error:", messageContent);
}
