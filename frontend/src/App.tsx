import Menu from "./components/Menu";
import MainStage from "./components/MainStage";
import { BlockI } from "./models/block.model";
import { generateShapes } from "./functions/generateInitShapes";
import React from "react";

function App() {
  const INITIAL_STATE: BlockI[] = generateShapes();
  const [blocks, setBlocks] = React.useState<BlockI[]>(INITIAL_STATE);

  return (
    <div>
      <Menu blocks={blocks} setBlocks={setBlocks} />
      <MainStage blocks={blocks} setBlocks={setBlocks} />
    </div>
  );
}

export default App;
