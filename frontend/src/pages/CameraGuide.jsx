import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./CameraGuide.css";

export default function CameraGuide() {
  const navigate = useNavigate();
  const [current, setCurrent] = useState(0);
  const [autoSlide, setAutoSlide] = useState(true);

  const slides = [
    {
      image: "/guide-1.png",
      text: "Hold phone in front of your face"
    },
    {
      image: "/guide-2.png",
      text: "Fit your face in the oval"
    },
    {
      image: "/guide-3.png",
      text: "Remove glasses"
    }
  ];

  // Continuous auto sliding every 2 seconds
  useEffect(() => {
    if (!autoSlide) return;

    const timer = setInterval(() => {
      setCurrent(prev => (prev + 1) % slides.length);
    }, 2000);

    return () => clearInterval(timer);
  }, [autoSlide]);

  const handleNext = () => {
    // Stop auto sliding when user interacts
    setAutoSlide(false);

    if (current === slides.length - 1) {
      navigate("/camera");
    } else {
      setCurrent(prev => prev + 1);
    }
  };

  return (
    <div className="guide-wrapper">

      

      <div className="guide-content">

        {/* SLIDER */}
        <div className="slider-container">
          <div
            className="slider-track"
            style={{ transform: `translateX(-${current * 100}%)` }}
          >
            {slides.map((slide, index) => (
              <div className="slide" key={index}>
                <img
                  src={slide.image}
                  alt="guide"
                  className="guide-image"
                />
                <h2>{slide.text}</h2>
              </div>
            ))}
          </div>
        </div>

        {/* Dots */}
        <div className="dots">
          {slides.map((_, index) => (
            <span
              key={index}
              className={current === index ? "dot active" : "dot"}
            ></span>
          ))}
        </div>

        {/* Always show Next */}
        <button className="next-btn" onClick={handleNext}>
          Next
        </button>

        <p className="secure-text">
          🔒 Secure Photo | Privacy Protected
        </p>

      </div>
    </div>
  );
}
