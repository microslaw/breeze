import { FrontendTypeEnum } from "../types/frontendType";

export interface ProcessingResultMetadataI {
  created_date?: string;
  datatype?: string;
  frontend_type?: FrontendTypeEnum;
  is_processed: boolean;
}
