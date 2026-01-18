import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import { Droplet, User, Weight, Activity, Cloud, MapPin } from "lucide-react";

// Components
import InputField from "./Components/InputField";
import CustomSelect from "./Components/CustomSelect";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  // State for form data
  const [formData, setFormData] = useState({
    age: "",
    gender: "",
    weight: "",
    daily_water_intake: "",
    physical_activity_level: "",
    weather: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [weatherLoading, setWeatherLoading] = useState(false);
  const [error, setError] = useState(null);

  // Handle Input Changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle Dropdown Changes
  const handleSelectChange = (name, value) => {
    setFormData({ ...formData, [name]: value });
  };

  // --- NEW: Weather Auto-Detection Logic ---
  const fetchWeather = () => {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported by your browser.");
      return;
    }

    setWeatherLoading(true);
    setError(null);

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        const API_KEY = process.env.REACT_APP_WEATHER_API_KEY;

        const API_URL = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&units=metric&appid=${API_KEY}`;

        try {
          const response = await axios.get(API_URL);
          const temp = response.data.main.temp;
          
          // Determine category based on temperature
          let weatherCategory = "Normal";
          if (temp < 15) weatherCategory = "Cold";
          else if (temp > 30) weatherCategory = "Hot";

          // Update state
          setFormData((prev) => ({ ...prev, weather: weatherCategory }));
        } catch (err) {
          console.error("Weather fetch error:", err);
          setError("Failed to fetch weather data. Please select manually.");
        } finally {
          setWeatherLoading(false);
        }
      },
      (err) => {
        console.error(err);
        setError("Location access denied or unavailable.");
        setWeatherLoading(false);
      }
    );
  };

  // Submit Logic
  const handleSubmit = async () => {
    if (Object.values(formData).some(x => x === "")) {
      setError("Please fill in all fields");
      setTimeout(() => setError(null), 3000);
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);

    const payload = {
      age: parseInt(formData.age),
      gender: formData.gender,
      weight: parseInt(formData.weight),
      daily_water_intake: parseFloat(formData.daily_water_intake),
      physical_activity_level: formData.physical_activity_level,
      weather: formData.weather
    };

    try {
      const response = await axios.post(`${BACKEND_URL}/predict`, payload);
      if (response.data && response.data.model_prediction) {
        setPrediction(response.data.model_prediction);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to get prediction. Please check server connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <div className="title-container">
          <Droplet size={40} color="#1E88E5" strokeWidth={2.5} />
          <h1 className="title">HydraSense</h1>
        </div>
        <p className="subtitle">
          Smart hydration insights powered by your daily habits and environment.
        </p>
        <div className="tags">
          <span className="tag"><Droplet size={16} /> Hydration Tracking</span>
          <span className="tag">ML-Powered</span>
          <span className="tag"><Activity size={16} /> Activity-Based</span>
        </div>
      </div>

      <div className="form-card">
        <div className="card-header">
          <div className="card-icon-container">
            <Droplet size={28} color="#1E88E5" strokeWidth={2.5} />
          </div>
          <h2 className="card-title">Hydration Level Prediction</h2>
          <p className="card-subtitle">Enter your metrics to get a prediction</p>
        </div>

        <div className="form-grid">
          <InputField
            label="Age"
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            placeholder="Enter your age"
            icon={<User size={16} color="#1E88E5" strokeWidth={2} />}
          />

          <CustomSelect
            label="Gender"
            options={['Male', 'Female']}
            value={formData.gender}
            onChange={(val) => handleSelectChange('gender', val)}
            icon={<User size={16} color="#1E88E5" strokeWidth={2} />}
          />

          <InputField
            label="Weight (kg)"
            type="number"
            name="weight"
            value={formData.weight}
            onChange={handleChange}
            placeholder="Enter your weight"
            icon={<Weight size={16} color="#1E88E5" strokeWidth={2} />}
          />

          <InputField
            label="Daily Water Intake (L)"
            type="number"
            name="daily_water_intake"
            value={formData.daily_water_intake}
            onChange={handleChange}
            placeholder="Enter water intake"
            icon={<Droplet size={16} color="#1E88E5" strokeWidth={2} />}
            step="0.1"
          />

          <div style={{ paddingTop: '16px' }}>
              <CustomSelect
                label="Physical Activity Level"
                options={['Low', 'Moderate', 'High']}
                value={formData.physical_activity_level}
                onChange={(val) => handleSelectChange('physical_activity_level', val)}
                icon={<Activity size={16} color="#1E88E5" strokeWidth={2} />}
              />
          </div>

          {/* Modified Weather Input Section */}
          <div className="weather-input-container">
             <div className="weather-header">
                <label className="input-label">
                  <span className="label-icon"><Cloud size={16} color="#1E88E5" strokeWidth={2} /></span>
                  Weather
                </label>
                <button 
                  className="detect-weather-btn" 
                  onClick={fetchWeather} 
                  disabled={weatherLoading}
                  type="button" // Prevent form submission
                >
                  {weatherLoading ? (
                    "Detecting..."
                  ) : (
                    <>
                      <MapPin size={12} /> Auto-Detect
                    </>
                  )}
                </button>
             </div>
             
             <CustomSelect
              label="" // Empty label because we used a custom header above
              options={['Cold', 'Normal', 'Hot']}
              value={formData.weather}
              onChange={(val) => handleSelectChange('weather', val)}
              icon={null} // Icon moved to header
            />
          </div>

        </div>

        <button className="submit-btn" onClick={handleSubmit} disabled={loading}>
          {loading ? "Analyzing..." : "Get Prediction"}
        </button>

        {prediction && (
          <div className={`result-overlay ${prediction === 'Poor' ? 'poor' : 'good'}`}>
            <div className="result-text">
              <strong>Hydration Status:</strong> {prediction}
            </div>
            <div className="result-subtext">
              {prediction === 'Good' 
                ? 'Great job! You\'re well-hydrated.' 
                : 'Consider increasing your water intake.'}
            </div>
          </div>
        )}

        {error && (
          <div className="result-overlay poor">
            <div className="result-text">{error}</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;