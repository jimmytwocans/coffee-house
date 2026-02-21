// src/components/CoffeeLoader.jsx
import React from "react";
import "./CoffeLoader.css";

const CoffeLoader = () => {
  return (
    <div className="coffee-loader-wrapper">
      <div className="coffee-loader">
        <div className="cup"></div>
        <div className="steam steam1"></div>
        <div className="steam steam2"></div>
        <div className="steam steam3"></div>
      </div>
    </div>
  );
};

export default CoffeLoader;
