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
