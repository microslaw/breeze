export interface SSEMessageI {
  type: SSEMessageType;
  content: SSEFinishedProcessingContentI;
}

export interface SSEFinishedProcessingContentI {
  node_id: number;
  processing_queue: number[];
}

export enum SSEMessageType {
  FinishedProcessing = "finished_processing",
  ProcessingError = "processing_error",
}
