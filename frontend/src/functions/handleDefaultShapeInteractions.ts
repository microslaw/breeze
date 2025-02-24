export const handleDragStart = (
  e: any,
  items: any[],
  setItems: React.Dispatch<React.SetStateAction<any[]>>
) => {
  const id = e.target.id();
  setItems(
    items.map((element) => ({
      ...element,
      isDragging: element.id === id,
    }))
  );
};

export const handleDragEnd = (
  e: any,
  items: any[],
  setItems: React.Dispatch<React.SetStateAction<any[]>>
) => {
  setItems(
    items.map((element) => {
      if (element.id === e.target.id()) {
        return {
          ...element,
          x: e.target.x(),
          y: e.target.y(),
          isDragging: false,
        };
      }
      return element;
    })
  );
};
