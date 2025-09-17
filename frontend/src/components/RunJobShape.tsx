// CONCEPT COMPONENT ONLY !!!
import { Group, RegularPolygon } from "react-konva";
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
  const handleRunJob = async () => {
    await runProcessingJob(id);
  };

  return (
    <Group>
      {show && (
        <RegularPolygon
          x={x}
          y={y}
          fill="green"
          stroke={"darkSlateGray"}
          strokeWidth={1}
          sides={3}
          rotation={90}
          lineJoin={"round"}
          radius={BLOCK_HEIGHT / 10}
          shadowColor="black"
          shadowBlur={3}
          shadowOpacity={0.5}
          draggable
          shadowOffsetX={0.7}
          shadowOffsetY={0.7}
          onClick={handleRunJob}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        />
      )}
    </Group>
  );
};

export default RunJobShape;
