// TODO split general sse model into separate by type interfaces
export interface SSEMessageI {
  type: SSEMessageType;
  content: SSEFinishedProcessingContentI | SSEProcessingErrorContentI;
}

export interface SSEFinishedProcessingContentI {
  node_id: number;
  processing_queue: number[];
}

export interface SSEProcessingErrorContentI {
  origin: {
    node_id: number;
    node_type: string;
  };
  trackback_string: string;
}

export enum SSEMessageType {
  FinishedProcessing = "finished_processing",
  ProcessingError = "processing_error",
}
