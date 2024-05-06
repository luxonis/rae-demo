import "./App.css";
import { ConnectionStatusRouter } from "./ConnectionStatusRouter";
import { VisualizerContainer } from "./VisualizerContainer";

function App() {
  return (
    <>
      <h1>RAE Demo</h1>
      <VisualizerContainer>
        <ConnectionStatusRouter />
      </VisualizerContainer>
    </>
  );
}

export default App;
