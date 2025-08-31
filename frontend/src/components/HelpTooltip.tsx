import { Modal, Button, Form, OverlayTrigger, Tooltip } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faQuestion } from "@fortawesome/free-solid-svg-icons";

interface HelpTooltipProps {
  content: string;
}

const HelpTooltip = ({ content }: HelpTooltipProps) => {
  const renderTooltip = (props: any) => (
    <Tooltip id="button-tooltip" {...props}>
      {content}
    </Tooltip>
  );

  return (
    <OverlayTrigger
      placement="right"
      delay={{ show: 150, hide: 400 }}
      overlay={renderTooltip}
    >
      <Button
        variant="primary"
        style={{
          borderRadius: "50%",
          width: "30px",
          height: "30px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: 0,
        }}
      >
        <FontAwesomeIcon icon={faQuestion} size="2xs" />
      </Button>
    </OverlayTrigger>
  );
};

export default HelpTooltip;
