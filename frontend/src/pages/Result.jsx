import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Result.css";

export default function Result() {
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState("concerns");
  const [selectedConcern, setSelectedConcern] = useState(null);
  const [selectedPriceRange, setSelectedPriceRange] = useState(null);
  const [selectedProductRoutine, setSelectedProductRoutine] = useState(null);
  const [analysisFlow, setAnalysisFlow] = useState("camera"); // Track flow type
  const navigate = useNavigate();

  // Price range categories
  const priceRanges = {
    budget: { label: "Budget (₹0-500)", min: 0, max: 500 },
    affordable: { label: "Affordable (₹501-1500)", min: 501, max: 1500 },
    premium: { label: "Premium (₹1501-3000)", min: 1501, max: 3000 },
    luxury: { label: "Luxury (₹3000+)", min: 3000, max: Infinity }
  };

  useEffect(() => {
    try {
      const data = JSON.parse(sessionStorage.getItem('analysisResult') || 'null');
      setResult(data);
      
      // Determine flow type from sessionStorage
      const flow = sessionStorage.getItem('analysisFlow') || 'camera';
      setAnalysisFlow(flow);
      
      console.log("Result data:", data);
    } catch (e) {
      console.error("Error parsing result:", e);
      setResult(null);
    }
  }, []);

  if (!result) {
    return (
      <div className="result-container">
        <div className="result-box">
          <div className="error-state">
            <h2>📊 No Analysis Found</h2>
            <p>Please analyze your skin first to see recommendations.</p>
            <button className="btn btn-primary" onClick={() => navigate('/guide')}>
              Go to Camera
            </button>
          </div>
        </div>
      </div>
    );
  }

  const concerns = result?.form?.concerns || [];
  const products = result?.form?.recommended_products || [];
  const productRoutines = result?.form?.product_routines || [];
  const skinType = result?.form?.skinType || "Unknown";

  // Get products for selected concern and price range
  const getFilteredProducts = () => {
    if (!selectedConcern) return [];
    let filtered = products.filter(p => p.concern === selectedConcern);
    
    if (selectedPriceRange) {
      const range = priceRanges[selectedPriceRange];
      filtered = filtered.filter(p => {
        const priceStr = p.price || "0";
        // Extract first number from price string (handles formats like "₹1800–₹2200")
        const priceMatch = priceStr.match(/\d+/);
        const price = priceMatch ? parseInt(priceMatch[0]) : 0;
        return price >= range.min && price <= range.max;
      });
    }
    
    return filtered;
  };

  const filteredProducts = getFilteredProducts();

  return (
    <div className="result-container">
      <div className="result-box">
        {/* Header */}
        <div className="result-header">
          <h1>✨ Your Skincare Analysis</h1>
          <p className="skin-type-badge">
            <span className="badge-label">Skin Type:</span>
            <span className="badge-value">{skinType}</span>
          </p>
          <p className="concerns-summary">
            <span className="concern-count">Selected Concerns:</span>
            {concerns.length > 0 ? (
              <span className="concerns-list">{concerns.map(c => c.charAt(0).toUpperCase() + c.slice(1)).join(", ")}</span>
            ) : (
              <span className="concerns-list">None selected</span>
            )}
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="tab-navigation">
          <button
            className={`tab-btn ${activeTab === "concerns" ? "active" : ""}`}
            onClick={() => setActiveTab("concerns")}
          >
            🎯 Your Concerns
          </button>
          <button
            className={`tab-btn ${activeTab === "products" ? "active" : ""}`}
            onClick={() => setActiveTab("products")}
          >
            🧴 Products ({filteredProducts.length})
          </button>
          <button
            className={`tab-btn ${activeTab === "routine" ? "active" : ""}`}
            onClick={() => setActiveTab("routine")}
          >
            📋 Routine
          </button>
        </div>

        {/* Tab Content */}

        {/* Concerns Tab - SHOWN FIRST */}
        {activeTab === "concerns" && (
          <div className="tab-content concerns-content">
            <h2>🎯 Your Selected Skin Concerns</h2>
            {concerns.length > 0 ? (
              <div className="concerns-grid">
                {concerns.map((concern, index) => (
                  <div 
                    key={index} 
                    className={`concern-card ${selectedConcern === concern ? "selected" : ""}`}
                    onClick={() => {
                      setSelectedConcern(concern);
                      setSelectedPriceRange(null);
                    }}
                  >
                    <div className="concern-icon">
                      {concern === "acne" && "🔴"}
                      {concern === "dark_spots" && "🟤"}
                      {concern === "dark spots" && "🟤"}
                      {concern === "dryness" && "💧"}
                      {concern === "wrinkles" && "✨"}
                      {concern === "pores" && "⚪"}
                      {concern === "blackheads" && "⚫"}
                      {concern === "pigmentation" && "🎨"}
                      {!["acne", "dark_spots", "dark spots", "dryness", "wrinkles", "pores", "blackheads", "pigmentation"].includes(concern) && "❓"}
                    </div>
                    <h3>{concern.charAt(0).toUpperCase() + concern.slice(1)}</h3>
                    <p className="concern-description">
                      {getConcernDescription(concern)}
                    </p>
                    <p className="product-count">
                      {products.filter(p => p.concern === concern).length} products available
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">No concerns selected. Your skin looks great! 💚</p>
            )}
          </div>
        )}

        {/* Price Range Selection - After Concern Selected */}
        {activeTab === "concerns" && selectedConcern && (
          <div className="price-range-section">
            <h3>Select Price Range for {selectedConcern.charAt(0).toUpperCase() + selectedConcern.slice(1)}</h3>
            <div className="price-range-grid">
              {Object.entries(priceRanges).map(([key, range]) => (
                <button
                  key={key}
                  className={`price-range-btn ${selectedPriceRange === key ? "active" : ""}`}
                  onClick={() => setSelectedPriceRange(key)}
                >
                  {range.label}
                </button>
              ))}
            </div>
            {selectedPriceRange && (
              <button 
                className="btn btn-primary"
                onClick={() => setActiveTab("products")}
              >
                View Products in {priceRanges[selectedPriceRange].label} →
              </button>
            )}
          </div>
        )}

        {/* Products Tab */}
        {activeTab === "products" && (
          <div className="tab-content products-content">
            <div className="products-header">
              <h2>🧴 Products for {selectedConcern ? selectedConcern.charAt(0).toUpperCase() + selectedConcern.slice(1) : "Selected Concern"}</h2>
              {selectedPriceRange && (
                <p className="price-filter-tag">💰 {priceRanges[selectedPriceRange].label}</p>
              )}
            </div>
            
            {filteredProducts.length > 0 ? (
              <div className="products-grid">
                {filteredProducts.map((product, index) => {
                  // Find matching routine by product name (case-insensitive)
                  const routine = productRoutines.find(r => 
                    r && r.product && r.product.toLowerCase() === product.product.toLowerCase()
                  );
                  return (
                    <div key={index} className="product-card">
                      <div className="product-header">
                        <h3>{product.product}</h3>
                        <span className="concern-badge">{product.concern.toUpperCase()}</span>
                      </div>
                      
                      <p className="product-description">{product.description}</p>
                      
                      <div className="product-details">
                        {product.ingredients && (
                          <div className="detail-item">
                            <span className="label">Ingredients:</span>
                            <p className="value">{product.ingredients}</p>
                          </div>
                        )}
                        
                        {product.price && (
                          <div className="detail-item">
                            <span className="label">Price:</span>
                            <p className="value price-value">{product.price}</p>
                          </div>
                        )}
                      </div>

                      <button 
                        className="btn-view-routine"
                        onClick={() => {
                          setSelectedProductRoutine(routine);
                          setActiveTab("routine");
                        }}
                      >
                        📋 View Skincare Routine →
                      </button>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="no-data">
                {selectedConcern ? `No products found in ${priceRanges[selectedPriceRange]?.label || 'selected price range'}.` : "Select a concern to view products."}
              </p>
            )}

            <button 
              className="btn btn-secondary"
              onClick={() => {
                setSelectedConcern(null);
                setSelectedPriceRange(null);
                setActiveTab("concerns");
              }}
            >
              ← Back to Concerns
            </button>
          </div>
        )}

        {/* Routine Tab - Shows Only Selected Product's Routine */}
        {activeTab === "routine" && (
          <div className="tab-content routine-content">
            {selectedProductRoutine ? (
              <div className="product-routine-card">
                <div className="routine-header">
                  <h2>💫 {selectedProductRoutine.product}</h2>
                  <p className="routine-concern">For: {selectedProductRoutine.concern.toUpperCase()}</p>
                  <p className="routine-description">{selectedProductRoutine.description}</p>
                </div>

                {/* Morning Routine */}
                <div className="routine-section">
                  <h3>🌅 Morning Routine</h3>
                  <div className="routine-steps">
                    {selectedProductRoutine.morning?.steps?.map((step, stepIndex) => (
                      <div key={stepIndex} className="routine-step">
                        <div className="step-number">{step.step_number}</div>
                        <div className="step-content">
                          <h5>{step.name}</h5>
                          <p className="step-description">{step.description}</p>
                          <p className="step-tip">💡 {step.tip}</p>
                          {step.product_focus && (
                            <p className="product-focus">⭐ Key step for {selectedProductRoutine.product}</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Evening Routine */}
                <div className="routine-section">
                  <h3>🌙 Evening Routine</h3>
                  <div className="routine-steps">
                    {selectedProductRoutine.evening?.steps?.map((step, stepIndex) => (
                      <div key={stepIndex} className="routine-step">
                        <div className="step-number">{step.step_number}</div>
                        <div className="step-content">
                          <h5>{step.name}</h5>
                          <p className="step-description">{step.description}</p>
                          <p className="step-tip">💡 {step.tip}</p>
                          {step.product_focus && (
                            <p className="product-focus">⭐ Key step for {selectedProductRoutine.product}</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <button 
                  className="btn btn-secondary"
                  onClick={() => setActiveTab("products")}
                >
                  ← Back to Products
                </button>
              </div>
            ) : (
              <p className="no-data">Select a product to view its skincare routine.</p>
            )}
          </div>
        )}

        {/* Action Buttons */}
        <div className="action-buttons">
          <button className="btn btn-secondary" onClick={() => navigate('/')}>
            🏠 Home
          </button>
          {activeTab !== "routine" && (
            <button 
              className="btn btn-primary" 
              onClick={() => {
                if (analysisFlow === 'upload') {
                  navigate('/upload');
                } else if (analysisFlow === 'chat') {
                  navigate('/chat');
                } else {
                  navigate('/guide');
                }
              }}
            >
              {analysisFlow === 'upload' ? '📤 Upload Again' : analysisFlow === 'chat' ? '💬 Chat Again' : '📸 Analyze Again'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

function getConcernDescription(concern) {
  const descriptions = {
    acne: "Inflammatory skin condition causing pimples, blackheads, and whiteheads",
    dark_spots: "Hyperpigmentation or post-inflammatory marks on the skin",
    "dark spots": "Hyperpigmentation or post-inflammatory marks on the skin",
    dryness: "Lack of moisture in the skin causing tightness and flaking",
    wrinkles: "Fine lines and creases indicating loss of skin elasticity",
    pores: "Enlarged or visible pores that need minimizing",
    blackheads: "Clogged pores with oxidized sebum appearing dark",
    pigmentation: "Uneven skin tone or excess melanin production"
  };
  return descriptions[concern] || "Skin concern requiring targeted treatment";
}
