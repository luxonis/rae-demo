import { toCanvas } from "qrcode";
import { memo, useEffect, useMemo, useRef } from "react";

const QR_CODE_WIDTH = 300;

export const QRCode = memo(function QRCode(props: { clientId: string }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const codeContent = useMemo(
    () => JSON.stringify({ client_id: props.clientId }),
    [props.clientId]
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
    </div>
  );
});
