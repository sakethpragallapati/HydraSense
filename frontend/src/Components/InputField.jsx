import React from "react";

const InputField = ({ label, type, name, value, onChange, placeholder, icon, step }) => {
  return (
    <div className="input-group">
      <label>
        {icon && <span className="label-icon">{icon}</span>}
        {label}
      </label>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        step={step}
        required
      />
    </div>
  );
};

export default InputField;