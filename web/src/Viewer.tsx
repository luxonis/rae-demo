import { useSourceControl, ImagePanel } from "depthai-visualizer";

function Controls() {
  const { callService } = useSourceControl();

  return (
    <div>
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

export function Viewer() {
  const panelId = "camera";

  return (
    <div style={{ height: "480px" }}>
      <Controls />
      <div style={{ display: "flex", height: "100%" }}>
        <ImagePanel panelId={panelId} imageTopic="/cam/color" />
      </div>
    </div>
  );
}
