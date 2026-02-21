import React from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

export default function Login() {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    toast.success("Login successful!"); // 
    navigate("/manage"); // After login, go to /manage page
  };

  const handleLogoClick = () => {
    navigate("/"); // If user clicks CoffeeHouse logo, go to home page
  };

  return (
    <div
      style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}
    >
      {/* CoffeeHouse Header */}
      <header
        className="navbar"
        style={{
          justifyContent: "left",
          padding: "1.5rem",
          backgroundColor: "#a14a3a",
          fontSize: "2rem",
          fontWeight: "bold",
          fontFamily: "'Garamond', serif",
          color: "white",
          cursor: "pointer", // Make it look clickable
        }}
        onClick={handleLogoClick} // <-- Clicking logo goes to home
      >
        CoffeeHouse
      </header>

      {/* Centered Login Form */}
      <div
        style={{
          flexGrow: 1,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <div className="login wrap">
          <div className="h1"> Manager Login</div>
          <form onSubmit={handleLogin}>
            <input
              pattern="^([a-zA-Z0-9_\\-\\.]+)@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.)|(([a-zA-Z0-9\\-]+\\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\\]?)$"
              placeholder="Email"
              id="email"
              name="email"
              type="text"
              required
            />
            <input
              placeholder="Password"
              id="password"
              name="password"
              type="password"
              required
            />
            <input value="Login" className="btn" type="submit" />
          </form>
        </div>
      </div>
    </div>
  );
}
