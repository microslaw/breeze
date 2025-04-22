import Menu from "./components/Menu";
import MainStage from "./components/MainStage";
import { BlockI } from "./models/block.model";
import { deleteNodeById, getAllNodes } from "./services/mainApiService";
import { useEffect, useState } from "react";
import BlockModalDetails from "./components/BlockModalDeatils";

function App() {
  const [blocks, setBlocks] = useState<BlockI[]>([]);

  useEffect(() => {
    console.log("App mounted");
    const fetchBlocks = async () => {
      const nodes = await getAllNodes();
      setBlocks(nodes);
    };
    fetchBlocks();
  }, []);

  const [isBlockModalDeatilsVisible, setIsBlockModalDeatilsVisible] =
    useState<boolean>(false);

  const [selectedBlock, setSelectedBlock] = useState<BlockI>({
    id: Math.floor(Math.random() * 1000000),
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

  const handleCloseBlockDetails = () => {
    setIsBlockModalDeatilsVisible(false);
  };

  const handleDeleteBlock = (blockId: number) => {
    deleteNodeById(blockId);
    setBlocks((prevBlocks) =>
      prevBlocks.filter((block) => block.id !== selectedBlock.id)
    );
    handleCloseBlockDetails();
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
        handleClose={() => handleCloseBlockDetails()}
        handleDelete={(blockId) => handleDeleteBlock(blockId)}
      />
    </div>
  );
}

export default App;
