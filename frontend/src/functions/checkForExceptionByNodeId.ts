import { getProcessingException } from "../services/processingApiService";

export default async function checkForExceptionByNodeId(
  nodeId: number
): Promise<string | undefined> {
  const exceptionMessage = await getProcessingException().then(
    (message: any) => {
      if (message && message.content.origin.node_id === nodeId) {
        console.log(
          "Checking for exception for node ID:",
          message.content.traceback_str
        );
        return message.content.traceback_str;
      }
    }
  );
  return exceptionMessage;
}
