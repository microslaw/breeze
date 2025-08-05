import axios from "axios";

// TODO assign response types to the functions
export async function getBlob(): Promise<string> {
  try {
    const response = await axios({
      method: "get",
      url: "http://127.0.0.1:5000/blob",
      responseType: "blob",
    });

    console.log(response);
    // Create a URL for the blob
    const blobUrl = URL.createObjectURL(response.data);
    console.log("Blob URL:", blobUrl);
    return blobUrl;
  } catch (error) {
    console.error("Error fetching blob:", error);
    throw error;
  }
}
