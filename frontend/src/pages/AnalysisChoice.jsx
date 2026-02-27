import { useNavigate } from "react-router-dom";
import "./AnalysisChoice.css";

export default function AnalysisChoice() {
  const navigate = useNavigate();

  return (
    <div className="analysis-choice-container">
      <div className="choice-box">
        <h2>How would you like to analyze your skin?</h2>

        <div className="choices">
          <div className="choice-card" onClick={() => navigate('/guide')}>
            <img src="/guide-1.png" alt="camera" />
            <h3>Camera Scan</h3>
            <p>Use your device camera to scan your face and get instant analysis.</p>
            <button className="choice-action">Start Camera</button>
          </div>

          <div className="choice-card" onClick={() => navigate('/upload')}>
            <img src="/hero-derma.png" alt="upload" />
            <h3>Upload Image</h3>
            <p>Upload a clear photo of your face from your gallery.</p>
            <button className="choice-action">Upload Photo</button>
          </div>

          <div className="choice-card" onClick={() => navigate('/chat')}>
            <img src="/guide-3.png" alt="chat" />
            <h3>Chat Bot</h3>
            <p>Describe your concerns to the bot and get personalized recommendations.</p>
            <button className="choice-action outline">Chat Now</button>
          </div>
        </div>

        <p className="note">You can choose camera scan or upload; chat bot uses typed concerns.</p>
      </div>
    </div>
  );
}
