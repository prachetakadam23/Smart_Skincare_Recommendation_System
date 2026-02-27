import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Camera.css";

export default function Camera() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const navigate = useNavigate();
  const [photoTaken, setPhotoTaken] = useState(false);

 useEffect(() => {
  let stream;

  const startCamera = async () => {
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user" }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (error) {
      alert("Camera access denied");
    }
  };

  startCamera();

  // 🔥 CLEANUP FUNCTION
  return () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }
  };
}, []);


  const capturePhoto = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    setPhotoTaken(true);

    // send image to backend analyze endpoint
    (async () => {
      try {
        // Convert canvas to blob directly
        canvas.toBlob(async (blob) => {
          if (!blob) {
            alert('Failed to capture image');
            return;
          }

          const fd = new FormData();
          fd.append('image', blob, 'capture.png');

        const analyzeResp = await fetch('/analyze', {
          method: 'POST',
          body: fd
        });

        if (!analyzeResp.ok) {
          alert('Analysis failed');
          return;
        }

        const analyzeJson = await analyzeResp.json();

        // get stored user profile
        let profile = null;
        try { profile = JSON.parse(sessionStorage.getItem('userProfile') || 'null'); } catch(e) { profile = null; }

        // model-predicted concerns (may be demo values)
        const predictedFromModel = analyzeJson.concerns || analyzeJson.predicted_concerns || (analyzeJson.recommendations ? String(analyzeJson.recommendations).split(/\s*,\s*/) : []);

        // prefer user-selected concerns saved in profile; fall back to model predictions
        const predicted = (profile?.concerns && Array.isArray(profile.concerns) && profile.concerns.length > 0)
          ? profile.concerns.map(c => String(c).toLowerCase().trim())
          : (Array.isArray(predictedFromModel) ? predictedFromModel.map(c => String(c).toLowerCase().trim()) : []);

        const payload = {
          skinType: profile?.skinType || '',
          ageGroup: profile?.ageGroup || '',
          concerns: predicted
        };

        // call analyze-form to get recommendations
        const formResp = await fetch('/analyze-form', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const formJson = await formResp.json();

        try { sessionStorage.setItem('analysisResult', JSON.stringify({ analyze: analyzeJson, form: formJson })); } catch(e){}
        try { sessionStorage.setItem('analysisFlow', 'camera'); } catch(e){}

        navigate('/result');
        }, 'image/png');
      } catch (err) {
        console.error(err);
        alert('Error sending image to backend');
      }
    })();
  };

  return (
    <div className="camera-wrapper">
      <div className="camera-box">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          className="video"
        />

        <div className="oval-overlay"></div>

        <canvas ref={canvasRef} style={{ display: "none" }} />
      </div>

      {!photoTaken ? (
        <button className="capture-btn" onClick={capturePhoto}>
          Capture
        </button>
      ) : (
        <button
          className="capture-btn"
          onClick={() => navigate("/result")}
        >
          Analyse Skin
        </button>
      )}

      <p className="secure-text">
        🔒 Secure Photo | Privacy Protected
      </p>
    </div>
  );
}
