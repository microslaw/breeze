import axios from "axios";

export default async function getNodeTypes() {
  const response = await axios({
    method: "get",
    url: "http://127.0.0.1:5000/nodeTypes",
    responseType: "stream",
  });
  console.log(response.data);
}
