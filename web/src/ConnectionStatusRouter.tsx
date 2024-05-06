import { useSourceControl } from "depthai-visualizer";
import { useEffect, useRef } from "react";
import { v4 as uuid } from "uuid";
import { Viewer } from "./Viewer";
import { QRCode } from "./QRCode";

export function ConnectionStatusRouter() {
  const clientId = useRef(uuid());
  const { status, selectSource } = useSourceControl();

  useEffect(() => {
    selectSource(clientId.current);
  }, [selectSource, clientId]);

  return status === "connected" ? (
    <Viewer clientId={clientId.current} />
  ) : (
    <QRCode clientId={clientId.current} />
  );
}
