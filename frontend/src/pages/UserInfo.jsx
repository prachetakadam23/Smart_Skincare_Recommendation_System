import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./UserInfo.css";

export default function UserInfo() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    age: "",
    gender: ""
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = () => {
    if (!formData.name || !formData.age || !formData.gender) {
      alert("Please fill all fields");
      return;
    }

    // persist user profile and go to analysis choice
    const profile = {
      name: formData.name,
      age: formData.age,
      gender: formData.gender
    };
    try { sessionStorage.setItem('userProfile', JSON.stringify(profile)); } catch(e){}
    navigate('/analysis-choice');
  };

  return (
    <div className="userinfo-container">
      <div className="userinfo-content">

        <h2>Let’s Get Started</h2>
        <p>Tell us a little about yourself</p>

        <input
          type="text"
          name="name"
          placeholder="Full Name"
          value={formData.name}
          onChange={handleChange}
        />

        <input
          type="number"
          name="age"
          placeholder="Age"
          value={formData.age}
          onChange={handleChange}
        />

        <div className="gender-title">Choose Your Gender</div>

        <div className="gender-options">
          <button
            type="button"
            className={formData.gender === "Female" ? "active" : ""}
            onClick={() =>
              setFormData({ ...formData, gender: "Female" })
            }
          >
            Female
          </button>

          <button
            type="button"
            className={formData.gender === "Male" ? "active" : ""}
            onClick={() =>
              setFormData({ ...formData, gender: "Male" })
            }
          >
            Male
          </button>
        </div>

        <button
          type="button"
          className="continue-btn"
          onClick={handleSubmit}
        >
          Continue
        </button>
      </div>
    </div>
  );
}
