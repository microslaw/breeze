import Menu from "./components/Menu";
import MainStage from "./components/MainStage";
import { BlockI } from "./models/block.model";
import {
  deleteLinkById,
  deleteNodeById,
  getAllLinks,
  getAllNodes,
} from "./services/mainApiService";
import { useEffect, useState } from "react";
import BlockModalDetails from "./components/BlockModalDetails";
import LinkModalDetails from "./components/LinkModalDetails";
import { LinkI } from "./models/link.model";
import assignLinksPositionByBlocksPosition from "./functions/assignLinksPositionByBlocksPosition";
import LinkModalCreate from "./components/LinkModalCreate";
import BlockModalCreate from "./components/BlockModalCreate";

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

  const [isBlockModalDetailsVisible, setIsBlockModalDetailsVisible] =
    useState<boolean>(false);

  const [isBlockModalCreateVisible, setIsBlockModalCreateVisible] =
    useState<boolean>(false);

  const [isLinkModalDeatilsVisible, setIsLinkModalDeatilsVisible] =
    useState<boolean>(false);

  const [isLinkModalCreateVisible, setIsLinkModalCreateVisible] =
    useState<boolean>(false);

  const [selectedBlock, setSelectedBlock] = useState<BlockI>({
    id: -1,
    name: "",
    type: "default",
    x: 0,
    y: 0,
    isDragging: false,
    isSelected: false,
    kwargs: [],
  });

  const [selectedLink, setSelectedLink] = useState<LinkI>({
    id: -1,
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
    setIsBlockModalDetailsVisible(true);
  };

  const handleLinkDoubleClick = (link: LinkI) => {
    setSelectedLink(link);
    setIsLinkModalDeatilsVisible(true);
  };

  const handleCloseBlockDetails = () => {
    setIsBlockModalDetailsVisible(false);
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
    deleteLinkById(linkId);
    setLinks((prevLinks) => prevLinks.filter((link) => link.id !== linkId));
    handleCloseLinkDetails();
  };

  return (
    <div>
      <Menu setIsBlockModalCreateVisible={setIsBlockModalCreateVisible} />
      {/* TODO add component wrapping MainStage and modals associated with its elements*/}
      <MainStage
        blocks={blocks}
        setBlocks={setBlocks}
        links={links}
        setLinks={setLinks}
        setSelectedLink={setSelectedLink}
        setIsBlockModalCreateVisible={setIsBlockModalCreateVisible}
        setIsLinkModalCreateVisible={setIsLinkModalCreateVisible}
        handleBlockDoubleClick={(block) => handleBlockDoubleClick(block)}
        handleLinkDoubleClick={(link) => handleLinkDoubleClick(link)}
      />
      <BlockModalDetails
        block={selectedBlock}
        setBlock={setSelectedBlock}
        show={isBlockModalDetailsVisible}
        handleClose={() => handleCloseBlockDetails()}
        handleDelete={(blockId) => handleDeleteBlock(blockId)}
      />
      <BlockModalCreate
        show={isBlockModalCreateVisible}
        handleClose={() => setIsBlockModalCreateVisible(false)}
        blocks={blocks}
        setBlocks={setBlocks}
      ></BlockModalCreate>
      <LinkModalDetails
        link={selectedLink}
        show={isLinkModalDeatilsVisible}
        handleClose={() => handleCloseLinkDetails()}
        handleDelete={(linkId) => handleDeleteLink(linkId)}
      />
      <LinkModalCreate
        show={isLinkModalCreateVisible}
        blocks={blocks}
        link={selectedLink}
        setLinks={setLinks}
        handleClose={() => setIsLinkModalCreateVisible(false)}
      />
    </div>
  );
}

export default App;
