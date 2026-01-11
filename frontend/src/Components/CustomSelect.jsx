import React, { useState, useRef, useEffect } from "react";

const CustomSelect = ({ label, options, value, onChange, icon }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown if clicked outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSelect = (option) => {
    onChange(option);
    setIsOpen(false);
  };

  return (
    <div className="input-group" ref={dropdownRef}>
      <label>
        {icon && <span className="label-icon">{icon}</span>}
        {label}
      </label>
      <div className="custom-select-container">
        <div 
          className={`custom-select-trigger ${value ? 'selected' : ''} ${isOpen ? 'open' : ''}`}
          onClick={() => setIsOpen(!isOpen)}
        >
          <span>{value || `Select ${label.toLowerCase()}`}</span>
          <span 
            className="select-arrow"
            style={{ transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)' }}
          >
            ▼
          </span>
        </div>
        {isOpen && (
          <div className="custom-select-options">
            {options.map((option) => (
              <div
                key={option}
                className="custom-option"
                onClick={() => handleSelect(option)}
              >
                {option}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CustomSelect;