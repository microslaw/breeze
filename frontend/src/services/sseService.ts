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
    const data: SSEMessageI = JSON.parse(e.data.replace(/'/g, '"'));
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
      if (block.id === selectedBlockRef.current.id) {
        setSelectedBlock(block);
      }
    });
    return updatedBlocks;
  });

  setProcessingQueue(processing_queue);
}
