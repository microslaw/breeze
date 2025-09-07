import { BlockI } from "../models/block.model";

export function handleWheel(e: any, stageRef: any) {
  e.evt.preventDefault();

  let direction = e.evt.deltaY > 0 ? 1 : -1;

  if (e.evt.ctrlKey) {
    direction = -direction;
  }
  zoomStage(direction, undefined, stageRef.current);
}

export function zoomStage(direction: number, step?: number, stage?: any) {
  if (!stage) return;
  const oldScale = stage.scaleX();
  const pointer = stage.getPointerPosition();

  const mousePointTo = {
    x: (pointer.x - stage.x()) / oldScale,
    y: (pointer.y - stage.y()) / oldScale,
  };

  if (!step) step = 2;
  const scaleBy = 1 + step / 100;
  const newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy;

  const newPos = {
    x: pointer.x - mousePointTo.x * newScale,
    y: pointer.y - mousePointTo.y * newScale,
  };

  stage.scale({ x: newScale, y: newScale });
  stage.position(newPos);
}

export function handleClick(
  e: any,
  setLastClickPosition: React.Dispatch<
    React.SetStateAction<{ x: number; y: number }>
  >,
  setIsSmallMenuVisible: React.Dispatch<React.SetStateAction<boolean>>,
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>
) {
  setLastClickPosition({ x: e.evt.layerX, y: e.evt.layerY });

  // button == 0 means left click
  if (e.evt.button === 0) {
    handleLeftClick(e, setIsSmallMenuVisible, blocks, setBlocks);
    // button == 2 means right click
  } else if (e.evt.button === 2) {
    handleRightClick(e, setIsSmallMenuVisible, setBlocks);
  }
}

function handleLeftClick(
  e: any,
  setIsSmallMenuVisible: React.Dispatch<React.SetStateAction<boolean>>,
  blocks: BlockI[],
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>
) {
  setIsSmallMenuVisible(false);

  if (e.target === e.target.getStage()) {
    setBlocks(
      blocks.map((b) => ({
        ...b,
        isSelected: false,
      }))
    );
  }
}

function handleRightClick(
  e: any,
  setIsSmallMenuVisible: React.Dispatch<React.SetStateAction<boolean>>,
  setBlocks: React.Dispatch<React.SetStateAction<BlockI[]>>
) {
  e.evt.preventDefault();
  if (e.target === e.target.getStage()) {
    setIsSmallMenuVisible(true);
  }
}
