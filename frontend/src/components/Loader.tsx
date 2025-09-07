import { Arc, Group } from "react-konva";
import { useEffect, useRef } from "react";
import { BLOCK_HEIGHT } from "../constants/ui";
import Konva from "konva";

interface LoaderProps {
  show: boolean;
  x: number;
  y: number;
}

const Loader = ({ show, x, y }: LoaderProps) => {
  const loaderRef = useRef<Konva.Arc>(null);

  useEffect(() => {
    const angularSpeed = 360;
    const anim = new Konva.Animation((frame) => {
      if (frame) {
        const angleDiff = (frame.timeDiff * angularSpeed) / 1000;
        loaderRef.current?.rotate(angleDiff);
      }
    }, loaderRef.current?.getLayer() || null);

    anim.start();

    return () => {
      anim.stop();
    };
  }, []);

  return (
    <Group>
      {show && (
        <Arc
          ref={loaderRef}
          x={x}
          y={y}
          fill="darkSlateGray"
          angle={100}
          innerRadius={BLOCK_HEIGHT / 20}
          outerRadius={BLOCK_HEIGHT / 10}
        />
      )}
    </Group>
  );
};

export default Loader;
