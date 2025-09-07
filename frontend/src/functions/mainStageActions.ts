export function handleWheel(e: any, stageRef: any) {
  e.evt.preventDefault();

  const stage: any = stageRef.current;
  if (!stage) return;
  const oldScale = stage.scaleX();
  const pointer = stage.getPointerPosition();

  const mousePointTo = {
    x: (pointer.x - stage.x()) / oldScale,
    y: (pointer.y - stage.y()) / oldScale,
  };

  let direction = e.evt.deltaY > 0 ? 1 : -1;

  if (e.evt.ctrlKey) {
    direction = -direction;
  }

  const scaleBy = 1.01;
  const newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy;

  const newPos = {
    x: pointer.x - mousePointTo.x * newScale,
    y: pointer.y - mousePointTo.y * newScale,
  };

  stage.scale({ x: newScale, y: newScale });
  stage.position(newPos);
}

export default function zoomStage(
  direction: number,
  step?: number,
  stage?: any
) {
  if (!stage) return;
  const oldScale = stage.scaleX();
  const pointer = stage.getPointerPosition();

  const mousePointTo = {
    x: (pointer.x - stage.x()) / oldScale,
    y: (pointer.y - stage.y()) / oldScale,
  };

  if (!step) step = 1;
  const scaleBy = 1 + step / 100;
  const newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy;

  const newPos = {
    x: pointer.x - mousePointTo.x * newScale,
    y: pointer.y - mousePointTo.y * newScale,
  };

  stage.scale({ x: newScale, y: newScale });
  stage.position(newPos);
}
