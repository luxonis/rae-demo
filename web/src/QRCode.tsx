import { toCanvas } from "qrcode";
import { useEffect, useRef } from "react";

const QR_CODE_WIDTH = 300;

export const QRCode = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (canvasRef.current) {
      const canvas = canvasRef.current;
      toCanvas(canvas, "https://www.luxonis.com", { width: QR_CODE_WIDTH });
    }
  }, [canvasRef]);

  return <canvas ref={canvasRef} />;
};
