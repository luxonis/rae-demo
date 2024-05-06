import { useSourceControl, ImagePanel } from "depthai-visualizer";

function Controls(props: { clientId: string }) {
  const { selectSource, callService } = useSourceControl();

  return (
    <div>
      <button
        style={{
          width: "80px",
          height: "30px",
          backgroundColor: "gray",
        }}
        onClick={() => selectSource(props.clientId)}
      >
        Connect
      </button>
      <button
        style={{
          width: "80px",
          height: "30px",
          backgroundColor: "gray",
        }}
        onClick={() => callService?.("depthai_demo", {})}
      >
        Call Service
      </button>
    </div>
  );
}

export function Viewer(props: { clientId: string }) {
  const panelId = "camera";

  return (
    <div style={{ height: "128px" }}>
      <Controls clientId={props.clientId} />
      <div style={{ display: "flex", height: "100%" }}>
        <ImagePanel panelId={panelId} imageTopic="/cam/color" />
      </div>
    </div>
  );
}
