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
import QueueModalDetails from "./components/QueueModalDetails";
import { getProcessingQueue } from "./services/processingApiService";
import { BLOCK_DEFAULT_COLOUR } from "./constants/ui";

function App() {
  const [blocks, setBlocks] = useState<BlockI[]>([]);
  const [links, setLinks] = useState<LinkI[]>([]);
  const [processingQueue, setProcessingQueue] = useState<number[]>([]);

  useEffect(() => {
    const fetchAppState = async () => {
      const blocks = await getAllNodes();
      const links = await getAllLinks();
      setBlocks(blocks);
      setLinks(links);
      assignLinksPositionByBlocksPosition(blocks, links);
    };
    fetchAppState();

    let interval: number | null = null;
    interval = setInterval(updateProcessingQueue, 1000);
  }, []);

  const [isBlockModalDetailsVisible, setIsBlockModalDetailsVisible] =
    useState<boolean>(false);

  const [isBlockModalCreateVisible, setIsBlockModalCreateVisible] =
    useState<boolean>(false);

  const [isLinkModalDeatilsVisible, setIsLinkModalDeatilsVisible] =
    useState<boolean>(false);

  const [isLinkModalCreateVisible, setIsLinkModalCreateVisible] =
    useState<boolean>(false);

  const [isQueueModalDetailsVisible, setIsQueueModalDetailsVisible] =
    useState<boolean>(false);

  const [selectedBlock, setSelectedBlock] = useState<BlockI>({
    id: -1,
    name: "",
    type: "default",
    x: 0,
    y: 0,
    isDragging: false,
    isSelected: false,
    isQueued: false,
    kwargs: [],
    colour: BLOCK_DEFAULT_COLOUR,
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

  function updateProcessingQueue() {
    getProcessingQueue().then((queue) => {
      setProcessingQueue(queue);
      setBlocks((prevBlocks) => {
        const updatedBlocks = [...prevBlocks];
        updatedBlocks.forEach((block) => {
          queue.find((item) => block.id === item)
            ? (block.isQueued = true)
            : (block.isQueued = false);
        });
        return updatedBlocks;
      });
    });
  }

  return (
    <div>
      <Menu
        setIsBlockModalCreateVisible={setIsBlockModalCreateVisible}
        setIsQueueModalDetailsVisible={setIsQueueModalDetailsVisible}
      />
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
      <QueueModalDetails
        show={isQueueModalDetailsVisible}
        handleClose={() => setIsQueueModalDetailsVisible(false)}
        processingQueue={processingQueue}
      ></QueueModalDetails>
    </div>
  );
}

export default App;
