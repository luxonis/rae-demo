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
      <div style={{ marginTop: "10px" }}>
        <button
          style={{ width: "80px", height: "30px", backgroundColor: "gray" }}
          onClick={() => alert("forward")}
        >
          Forward
        </button>
      </div>
      <div style={{ marginTop: "10px" }}>
        <button
          style={{
            width: "80px",
            height: "30px",
            backgroundColor: "gray",
            marginRight: "10px",
          }}
          onClick={() => alert("left")}
        >
          Left
        </button>
        <button
          style={{ width: "80px", height: "30px", backgroundColor: "gray" }}
          onClick={() => alert("right")}
        >
          Right
        </button>
      </div>
      <div style={{ marginTop: "10px" }}>
        <button
          style={{ width: "80px", height: "30px", backgroundColor: "gray" }}
          onClick={() => alert("backward")}
        >
          Backward
        </button>
      </div>
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
