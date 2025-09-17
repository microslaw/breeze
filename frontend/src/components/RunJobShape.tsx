import { Group, RegularPolygon } from "react-konva";
import { useState } from "react";
import { BLOCK_HEIGHT } from "../constants/ui";
import { runProcessingJob } from "../services/processingApiService";
import {
  handleMouseEnter,
  handleMouseLeave,
} from "../functions/handleDefaultShapeInteractions";

interface RunJobShapeProps {
  show: boolean;
  x: number;
  y: number;
  id: number;
}

const RunJobShape = ({ show, x, y, id }: RunJobShapeProps) => {
  const [pressed, setPressed] = useState(false);

  const handleRunJob = async () => {
    await runProcessingJob(id);
  };

  const scale = pressed ? 0.9 : 1;
  const fill = pressed ? "#197148ff" : "green";

  return (
    <Group>
      {show && (
        <RegularPolygon
          x={x}
          y={y}
          fill={fill}
          stroke={"darkSlateGray"}
          strokeWidth={1}
          sides={3}
          rotation={90}
          lineJoin={"round"}
          radius={BLOCK_HEIGHT / 8}
          shadowColor="black"
          shadowBlur={3}
          shadowOpacity={0.5}
          shadowOffsetX={0.7}
          shadowOffsetY={0.7}
          scaleX={scale}
          scaleY={scale}
          onClick={handleRunJob}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={(e) => {
            handleMouseLeave(e);
            setPressed(false);
          }}
          onMouseDown={() => setPressed(true)}
          onMouseUp={() => setPressed(false)}
        />
      )}
    </Group>
  );
};

export default RunJobShape;
