import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Camera.css";

export default function CameraUpload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFile = (e) => {
    const f = e.target.files[0];
    setFile(f);
  };

  const submitUpload = async () => {
    if (!file) return alert('Please choose an image to upload');
    setLoading(true);
    try {
      const fd = new FormData();
      fd.append('image', file, file.name || 'upload.png');

      const analyzeResp = await fetch('/analyze', { method: 'POST', body: fd });
      if (!analyzeResp.ok) throw new Error('Analyze failed');
      const analyzeJson = await analyzeResp.json();

      // get stored user profile
      let profile = null;
      try { profile = JSON.parse(sessionStorage.getItem('userProfile') || 'null'); } catch(e) { profile = null; }

      const payload = {
        skinType: profile?.skinType || '',
        ageGroup: profile?.ageGroup || '',
        concerns: (profile?.concerns && profile.concerns.length>0) ? profile.concerns : (analyzeJson.concerns || analyzeJson.predicted_concerns || [])
      };

      const formResp = await fetch('/analyze-form', {
        method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)
      });
      const formJson = await formResp.json();

      try { sessionStorage.setItem('analysisResult', JSON.stringify({ analyze: analyzeJson, form: formJson })); } catch(e){}
      try { sessionStorage.setItem('analysisFlow', 'upload'); } catch(e){}
      navigate('/result');
    } catch (err) {
      console.error(err);
      alert('Upload or analysis failed');
    } finally { setLoading(false); }
  };

  return (
    <div className="camera-wrapper" style={{background: '#F8F6F3'}}>
      <div className="camera-box upload-box" style={{background: 'white', color:'#222'}}>
        <h2 style={{color:'#D9BBE8'}}>Upload Face Image</h2>
        <p style={{color:'#666'}}>Choose a clear frontal photo of your face for best results.</p>
        <input type="file" accept="image/*" onChange={handleFile} />
        <div style={{marginTop:16, display:'flex', gap:12, flexWrap:'wrap'}}>
          <button className="capture-btn" onClick={submitUpload} disabled={loading} style={{background:'linear-gradient(90deg,#FFB6D9,#D9BBE8)', padding:'12px 20px', borderRadius:12}}>
            {loading ? 'Uploading...' : 'Upload & Analyze'}
          </button>
          <button className="capture-btn outline" onClick={() => navigate('/guide')} style={{background:'transparent', color:'#D9BBE8', border:'2px solid rgba(217,187,232,0.3)'}}>Use Camera Instead</button>
        </div>
      </div>
    </div>
  );
}
