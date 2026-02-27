import { useState, useRef, useEffect } from "react";
import "./Chat.css";
import { useNavigate } from "react-router-dom";


export default function Chat() {
  const bottomRef = useRef(null);
  const navigate = useNavigate();


  const skinTypes = ["Oily", "Dry", "Combination", "Normal"];

  const concernsList = [
    "Dryness",
    "Pigmentation",
    "Acne",
    "Wrinkles",
    "Pores",
    "Dark Spots",
    "Blackheads"
  ];

  const [messages, setMessages] = useState([]);
  const [step, setStep] = useState("intro");
  const [selectedConcerns, setSelectedConcerns] = useState([]);
  const [skinType, setSkinType] = useState("");
  const [duration, setDuration] = useState("");
  const [allergy, setAllergy] = useState("");
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    // Initial greeting
    setTimeout(() => {
      setIsTyping(false);
      setMessages([
        { type: "bot", text: "Hello 👋 This is Skinify. Let’s begin your skin transformation journey." }
      ]);

      setTimeout(() => {
        setIsTyping(true);
        setTimeout(() => {
          setIsTyping(false);
          
          setStep("ready");
        }, 900);
      }, 800);
    }, 1000);
  }, []);

 


  const botMessage = (text, nextStep = null) => {
    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);
      setMessages(prev => [...prev, { type: "bot", text }]);
      if (nextStep) setStep(nextStep);
    }, 900);
  };

  const startChat = () => {
    botMessage("First, tell me your skin type.", "skintype");
  };

  const selectSkinType = (type) => {
    setMessages(prev => [...prev, { type: "user", text: type }]);
    setSkinType(type);
    botMessage("Now select up to 3 major skin concerns.", "concerns");
  };

  const toggleConcern = (item) => {
    if (selectedConcerns.includes(item)) {
      setSelectedConcerns(
        selectedConcerns.filter(c => c !== item)
      );
    } else {
      if (selectedConcerns.length < 3) {
        setSelectedConcerns([...selectedConcerns, item]);
      }
    }
  };

  const confirmConcerns = () => {
    setMessages(prev => [
      ...prev,
      { type: "user", text: selectedConcerns.join(", ") }
    ]);
    botMessage("How long have you had this condition?", "duration");
  };

  const selectDuration = (text) => {
    setMessages(prev => [...prev, { type: "user", text }]);
    setDuration(text);
    botMessage("Do you have any allergies?", "allergy");
  };

  const submitAllergy = (e) => {
    if (e.key === "Enter") {
      const val = e.target.value || "No allergies";
      setMessages(prev => [
        ...prev,
        { type: "user", text: val }
      ]);
      setAllergy(val);
      botMessage("Great. Now please click your picture for analysis 📸", "camera");
    }
  };

  return (
    <div className="chat-container">

      {messages.map((msg, index) => (
        <div key={index} className={`message ${msg.type}`}>
          {msg.text}
        </div>
      ))}

      {isTyping && (
        <div className="message bot typing">
          <span></span>
          <span></span>
          <span></span>
        </div>
      )}

      {step === "ready" && (
        <button className="start-btn" onClick={startChat}>
          Get Started
        </button>
      )}

      {step === "skintype" && (
        <div className="option-group">
          {skinTypes.map(type => (
            <button key={type} onClick={() => selectSkinType(type)}>
              {type}
            </button>
          ))}
        </div>
      )}

      {step === "concerns" && (
        <>
          <div className="concern-grid">
            {concernsList.map(item => (
              <div
                key={item}
                className={`concern-chip ${
                  selectedConcerns.includes(item) ? "active" : ""
                }`}
                onClick={() => toggleConcern(item)}
              >
                {item}
              </div>
            ))}
          </div>

          {selectedConcerns.length > 0 && (
            <button className="start-btn" onClick={confirmConcerns}>
              Done
            </button>
          )}
        </>
      )}

      {step === "duration" && (
        <div className="option-group">
          <button onClick={() => selectDuration("Less than 6 months")}>
            Less than 6 months
          </button>
          <button onClick={() => selectDuration("More than 6 months")}>
            More than 6 months
          </button>
        </div>
      )}

      {step === "allergy" && (
        <input
          type="text"
          placeholder="Type here and press Enter..."
          className="chat-input"
          onKeyDown={submitAllergy}
        />
      )}

      {step === "camera" && (
        <button
          className="start-btn"
          onClick={async () => {
            // save collected profile
            const profile = {
              skinType,
              ageGroup: duration,
              concerns: selectedConcerns,
              allergy
            };
            try { sessionStorage.setItem('userProfile', JSON.stringify(profile)); } catch(e){}

            // prepare payload for form analysis (chat path: no image)
            const payload = {
              skinType: profile.skinType || '',
              ageGroup: profile.ageGroup || '',
              concerns: (Array.isArray(profile.concerns) ? profile.concerns.map(c => String(c).toLowerCase().trim()) : [])
            };

            try {
              const resp = await fetch('/analyze-form', {
                method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)
              });
              const formJson = await resp.json();
              // store result similar to camera flow (no analyze image)
              try { sessionStorage.setItem('analysisResult', JSON.stringify({ analyze: {}, form: formJson })); } catch(e){}
              try { sessionStorage.setItem('analysisFlow', 'chat'); } catch(e){}
              navigate('/result');
            } catch (err) {
              console.error(err);
              alert('Analysis failed');
            }
          }}
        >
          Get Recommendations
        </button>
      )}


      <div ref={bottomRef}></div>
    </div>
  );
}
