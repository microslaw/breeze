import FrontendType from "../types/frontendType";

export interface ProcessingResultMetadataI {
  created_date?: string;
  datatype?: string;
  frontend_type?: FrontendType;
  is_processed: boolean;
}
