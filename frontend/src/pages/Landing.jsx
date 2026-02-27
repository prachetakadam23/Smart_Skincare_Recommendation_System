import { useNavigate } from "react-router-dom";
import "./Landing.css";

export default function Landing() {
  const navigate = useNavigate();

  const philosophyData = [
    {
      img: "/Philosophy_1.png",
      icon: "🧬",
      title: "Root Cause Based",
      desc: "We treat skin from inside-out, identifying the real cause."
    },
    {
      img: "/Philosophy_2.png",
      icon: "👩‍⚕️",
      title: "Smart Dermatology Engine",
      desc: "AI-powered engine combining live image capture and convolutional neural networks for precise skin evaluation."
    },
    {
      img: "/Philosophy_3.png",
      icon: "🎯",
      title: "Personalised Treatment",
      desc: "Treatments designed uniquely for your skin type."
    },
    {
      img: "/Philosophy_4.png",
      icon: "🔒",
      title: "Secure & Ethical AI",
      desc: "Your photos are processed securely with privacy protection."
    }
  ];

  return (
    <div className="home">

      {/* HERO SECTION */}
      <section className="hero">
        <div className="hero-left">

          <h2 className="brand-name">Skinify</h2>
          <p className="hero-sub">AI Powered Dermatology</p>

          <h1>Prescription Treatment for Skin</h1>

          <button 
            className="primary-btn"
            onClick={() => navigate("/userinfo")}
          >
            Start Here
          </button>

        </div>

        <div className="hero-right">
          <img
            src="/hero-derma.png"
            alt="Dermatologist"
            className="hero-image"
          />
        </div>
      </section>

      {/* PHILOSOPHY */}
      <section className="philosophy">
        <h2>Our Treatment Philosophy</h2>

        <div className="philosophy-grid">
          {philosophyData.map((item, index) => (
            <div className="philosophy-card" key={index}>
              <img src={item.img} alt={item.title} />
              <div className="icon-badge">{item.icon}</div>
              <h3>{item.title}</h3>
              <p>{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* FINAL CTA */}
      <section className="final-cta">
        <h2>Ready to Start Your Journey?</h2>
        <p>
          Begin your AI-powered skin analysis and receive
          personalised recommendations designed just for you.
        </p>

        <button 
          className="primary-btn"
          onClick={() => navigate("/userinfo")}
        >
          Start Your AI Analysis
        </button>
      </section>

    </div>
  );
}
