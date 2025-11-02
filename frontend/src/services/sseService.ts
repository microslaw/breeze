import { BlockI } from "../models/block.model";
import { SSEMessageI, SSEMessageType } from "../models/ssemessage.model";

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
    console.log("SSE Event:", e.data);
    const data: SSEMessageI = JSON.parse(e.data);
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
        message,
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
      alert("Processing error:" + message.content);
      console.error("Processing error:", message.content);
      break;
    }
    default:
      console.error("Unknown message type:", message.type);
      break;
  }
}

function handleMessageTypeFinishedProcessing(
  message: SSEMessageI,
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>,
  processingQueue: number[],
  setProcessingQueue: React.Dispatch<React.SetStateAction<number[]>>,
  selectedBlockRef: React.MutableRefObject<BlockI>,
  setSelectedBlock: React.Dispatch<React.SetStateAction<BlockI>>
) {
  const { node_id, processing_queue } = message.content;

  setBlocks((prevBlocks) => {
    const updatedBlocks = [...prevBlocks];
    updatedBlocks.forEach((block) => {
      if (block.id === node_id) {
        block.isQueued = false;
        block.isProcessed = true;
      }
      console.log("Processing queue check for block id:", block.id);
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
