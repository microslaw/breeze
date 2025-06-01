import Menu from "./components/Menu";
import MainStage from "./components/MainStage";
import { BlockI } from "./models/block.model";
import {
  deleteNodeById,
  getAllLinks,
  getAllNodes,
} from "./services/mainApiService";
import { useEffect, useState } from "react";
import BlockModalDetails from "./components/BlockModalDeatils";
import LinkModalDetails from "./components/LinkModalDetails";
import { LinkI } from "./models/link.model";
import assignLinksPositionByBlocksPosition from "./functions/assignLinksPositionByBlocksPosition";

function App() {
  const [blocks, setBlocks] = useState<BlockI[]>([]);
  const [links, setLinks] = useState<LinkI[]>([]);

  useEffect(() => {
    console.log("App mounted");
    const fetchAppState = async () => {
      const blocks = await getAllNodes();
      const links = await getAllLinks();
      setBlocks(blocks);
      setLinks(links);
      assignLinksPositionByBlocksPosition(blocks, links);
    };
    fetchAppState();
  }, []);

  const [isBlockModalDeatilsVisible, setIsBlockModalDeatilsVisible] =
    useState<boolean>(false);

  const [isLinkModalDeatilsVisible, setIsLinkModalDeatilsVisible] =
    useState<boolean>(false);

  const [selectedBlock, setSelectedBlock] = useState<BlockI>({
    id: -1,
    name: "",
    type: "default",
    x: 0,
    y: 0,
    isDragging: false,
  });

  const [selectedLink, setSelectedLink] = useState<LinkI>({
    destinationNodeId: 0,
    destinationNodeInput: "",
    originNodeId: 0,
    originNodeOutput: "",
    startX: 0,
    startY: 0,
    endX: 0,
    endY: 0,
  });

  const handleBlockDoubleClick = (block: BlockI) => {
    setSelectedBlock(block);
    setIsBlockModalDeatilsVisible(true);
  };

  const handleLinkDoubleClick = (link: LinkI) => {
    setSelectedLink(link);
    setIsLinkModalDeatilsVisible(true);
  };

  const handleCloseBlockDetails = () => {
    setIsBlockModalDeatilsVisible(false);
  };

  const handleCloseLinkDetails = () => {
    setIsLinkModalDeatilsVisible(false);
  };

  const handleDeleteBlock = (blockId: number) => {
    deleteNodeById(blockId);
    setBlocks((prevBlocks) =>
      prevBlocks.filter((block) => block.id !== selectedBlock.id)
    );
    setLinks((prevLinks) =>
      prevLinks.filter(
        (link) =>
          link.originNodeId !== selectedBlock.id &&
          link.destinationNodeId !== selectedBlock.id
      )
    );
    handleCloseBlockDetails();
  };

  const handleDeleteLink = (linkId: number) => {
    console.info("Delete link not implemented yet");
  };

  return (
    <div>
      <Menu blocks={blocks} setBlocks={setBlocks} />
      {/* TODO add component wrapping MainStage and modals associated with its elements*/}
      <MainStage
        blocks={blocks}
        setBlocks={setBlocks}
        links={links}
        setLinks={setLinks}
        handleBlockDoubleClick={(block) => handleBlockDoubleClick(block)}
        handleLinkDoubleClick={(link) => handleLinkDoubleClick(link)}
      />
      <BlockModalDetails
        block={selectedBlock}
        show={isBlockModalDeatilsVisible}
        handleClose={() => handleCloseBlockDetails()}
        handleDelete={(blockId) => handleDeleteBlock(blockId)}
      />
      <LinkModalDetails
        link={selectedLink}
        show={isLinkModalDeatilsVisible}
        handleClose={() => handleCloseLinkDetails()}
        handleDelete={(linkId) => handleDeleteLink(linkId)}
      />
    </div>
  );
}

export default App;
