import { toCanvas } from "qrcode";
import { memo, useEffect, useMemo, useRef, useState } from "react";

const QR_CODE_WIDTH = 500;

export const QRCode = memo(function QRCode(props: { clientId: string }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [ssid, setSsid] = useState<string>("luxonis");
  const [password, setPassword] = useState<string | null>();

  const codeContent = useMemo(
    () => JSON.stringify({ client_id: props.clientId, ssid, password }),
    [props.clientId, ssid, password]
  );

  useEffect(() => {
    if (canvasRef.current) {
      const canvas = canvasRef.current;
      toCanvas(canvas, codeContent, { width: QR_CODE_WIDTH });
    }
  }, [canvasRef, codeContent]);

  return (
    <div>
      <canvas ref={canvasRef} />
      <div>
        <div style={{ marginTop: "10px" }}>
          <label style={{ marginRight: "10px" }}>Username</label>
          <input
            value={ssid}
            onChange={(evt) => setSsid(evt.target.value)}
          ></input>
        </div>
        <div style={{ marginTop: "10px" }}>
          <label style={{ marginRight: "5px" }}>Password (optional)</label>
          <input onChange={(evt) => setPassword(evt.target.value)}></input>
        </div>
      </div>

      {/* four controls for driving a robotic vehicle */}
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
});
