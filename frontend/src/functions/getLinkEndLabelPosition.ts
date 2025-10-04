export default function getLinkEndLabelPosition(
  startX: number,
  startY: number,
  endX: number,
  endY: number
): { x: number; y: number } {
  const dx = endX - startX;
  const dy = endY - startY;
  const length = Math.sqrt(dx * dx + dy * dy) || 1;

  const offset = 40;
  return {
    x: endX - (dx / length) * offset,
    y: endY + 3 - (dy / length) * offset,
  };
}
