import Menu from "./components/Menu";
import MainStage from "./components/MainStage";
import { BlockI } from "./models/block.model";
import { generateShapes } from "./functions/generateInitShapes";
import { useState } from "react";
import BlockModalDetails from "./components/BlockModalDeatils";

function App() {
  const INITIAL_STATE: BlockI[] = generateShapes();
  const [blocks, setBlocks] = useState<BlockI[]>(INITIAL_STATE);
  const [isBlockModalDeatilsVisible, setIsBlockModalDeatilsVisible] =
    useState<boolean>(false);

  const [selectedBlock, setSelectedBlock] = useState<BlockI>({
    id: "",
    name: "",
    type: "default",
    x: 0,
    y: 0,
    isDragging: false,
  });

  const handleBlockDoubleClick = (block: BlockI) => {
    setSelectedBlock(block);
    setIsBlockModalDeatilsVisible(true);
  };

  return (
    <div>
      <Menu blocks={blocks} setBlocks={setBlocks} />
      {/* TODO add component wrapping MainStage and modals associated with its elements*/}
      <MainStage
        blocks={blocks}
        setBlocks={setBlocks}
        handleBlockDoubleClick={(block) => handleBlockDoubleClick(block)}
      />
      <BlockModalDetails
        block={selectedBlock}
        show={isBlockModalDeatilsVisible}
        handleClose={() => setIsBlockModalDeatilsVisible(false)}
      />
    </div>
  );
}

export default App;
