import { Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";
import UserInfo from "./pages/UserInfo";
import Chat from "./pages/Chat";
import CameraGuide from "./pages/CameraGuide";
import Camera from "./pages/Camera";
import Result from "./pages/Result";
import AnalysisChoice from "./pages/AnalysisChoice";
import CameraUpload from "./pages/CameraUpload";





function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/userinfo" element={<UserInfo />} />
      <Route path="/chat" element={<Chat />} />
      <Route path="/analysis-choice" element={<AnalysisChoice />} />
      <Route path="/guide" element={<CameraGuide />} />
      <Route path="/camera" element={<Camera />} />
      <Route path="/upload" element={<CameraUpload />} />
      <Route path="/result" element={<Result />} />

    </Routes>
  );
}

export default App;
