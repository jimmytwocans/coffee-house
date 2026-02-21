import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom/client";
import "./Home.css";
import Login from "./Login";
import CoffeLoader from "../components/CoffeLoader";
import OrderSummaryModal from "../components/OrderSummaryModal";
import { fetchMenuItems, callOpenAILLM, placeOrder,fetchBaristas } from "../api/api";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { toast } from "react-toastify";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
    </Routes>
  </BrowserRouter>
);

export default function Home() {
  const [loading, setLoading] = useState(true);
  const [menuItems, setMenuItems] = useState([]);
  const [quantities, setQuantities] = useState({});
  const [facts, setFacts] = useState({});
  const [activeFactItem, setActiveFactItem] = useState(null);
  const [showModal, setShowModal] = useState(false);
  // const [baristas, setBaristas] = useState([]);
  const [currentBarista, setCurrentBarista] = useState(null);

  useEffect(() => {
    async function loadBaristas() {
      try {
        const data = await fetchBaristas(); // assume already returns JSON
        const now = new Date();
        const currentDay = now.toLocaleDateString("en-US", { weekday: "long" });

        const currentTime = now.toTimeString().slice(0, 5); // "HH:MM"
        const found = data.find((barista) => {
          if (!barista.days_working?.includes(currentDay)) return false;

          return (
            barista.start_time <= currentTime && barista.end_time >= currentTime
          );
        });

        setCurrentBarista(
          found || {
            ssn: "987-65-4321",
            name: "Bob Barista",
            email: "bob@coffe.com",
          }
        );
      } catch (e) {
        console.error("Failed to load baristas", e);
      }
    }


    loadBaristas();
  }, []);


  useEffect(() => {
    async function loadMenu() {
      const data = await fetchMenuItems();
      setMenuItems(data);
    }
    loadMenu();
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 2000);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest(".fact-popup") && !e.target.closest(".fact-icon")) {
        setActiveFactItem(null);
      }
    };
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, []);

  const handleQuantityChange = (itemName, delta) => {
    setQuantities((prev) => ({
      ...prev,
      [itemName]: Math.max(0, (prev[itemName] || 0) + delta),
    }));
  };

  const handleFetchFact = async (itemName) => {
    if (facts[itemName]) {
      setActiveFactItem(itemName === activeFactItem ? null : itemName);
      return;
    }

    try {
      const result = await callOpenAILLM(itemName); // already returns { text }

      setFacts((prev) => ({
        ...prev,
        [itemName]: result, // directly use result without parsing
      }));
      setActiveFactItem(itemName);
    } catch (err) {
      console.error("Failed to fetch fact:", err);
    }
  };


  const categorizedItems = {
    hot: [],
    cold: [],
    snack: [],
  };

  menuItems.forEach((item) => {
    if (item.hot_or_cold === "hot") categorizedItems.hot.push(item);
    else if (item.hot_or_cold === "cold") categorizedItems.cold.push(item);
    if (item.type === "snack" || item.type === "dessert")
      categorizedItems.snack.push(item);
  });

  if (loading) return <CoffeLoader />;

  const renderItems = (items) =>
    items.map((item, i) => (
      <div className="product-card no-image" key={i}>
        <h3>{item.name}</h3>
        <p>
          <strong>Size:</strong> {item.size} <br />
          <strong>Type:</strong> {capitalize(item.type)} <br />
          <strong>Temperature:</strong> {capitalize(item.hot_or_cold)} <br />
          <strong>Price:</strong> ${item.price}
        </p>
        <div className="product-footer" style={{ position: "relative" }}>
          <div className="qty-controls">
            <button onClick={() => handleQuantityChange(item.name, -1)}>
              -
            </button>
            <span>{quantities[item.name] || 0}</span>
            <button onClick={() => handleQuantityChange(item.name, 1)}>
              +
            </button>

            <button
              className="fact-icon"
              title="Interesting Fact"
              onClick={(e) => {
                e.stopPropagation();
                handleFetchFact(item.name);
              }}
            >
              💡
            </button>
          </div>

          {activeFactItem === item.name && facts[item.name] && (
            <div className="fact-popup">
              <p>{facts[item.name].text}</p>
            </div>
          )}
        </div>
      </div>
    ));

  return (
    <>
      <div className="home-container">
        <header className="hero">
          <div className="navbar">
            <div className="logo">CoffeeHouse</div>
            <nav>
              <a href="#">About</a>
              <Link to="/login">Login</Link>
            </nav>
          </div>
          <div className="hero-text">
            <h1>We serve the richest coffee in the city!</h1>
          </div>
          {currentBarista && (
            <div className="barista-profile">👤 {currentBarista.name}</div>
          )}
        </header>

        <section className="icons">
          <div className="icon">☕ Hot Coffee</div>
          <div className="icon">🧊 Cold Drinks</div>
          <div className="icon">🍵 Tea Cup</div>
          <div className="icon">🍰 Desserts</div>
        </section>

        <section className="section">
          <h2>Hot Coffee</h2>
          <div className="product-list">
            {renderItems(categorizedItems.hot)}
          </div>
        </section>

        <section className="section">
          <h2>Cold Drinks</h2>
          <div className="product-list">
            {renderItems(categorizedItems.cold)}
          </div>
        </section>

        <section className="section">
          <h2>Snacks</h2>
          <div className="product-list">
            {renderItems(categorizedItems.snack)}
          </div>
        </section>

        <div style={{ textAlign: "center", margin: "40px" }}>
          <button
            className="order-now-button"
            onClick={() => setShowModal(true)}
          >
            Order Now ({Object.values(quantities).reduce((a, b) => a + b, 0)})
          </button>
        </div>

        {showModal && (
          <OrderSummaryModal
            orderList={menuItems.filter((i) => quantities[i.name] > 0)}
            quantities={quantities}
            onClose={() => setShowModal(false)}
            onConfirm={async (paymentMethod) => {
              try {
                const order_info = menuItems
                  .filter((item) => quantities[item.name] > 0)
                  .map((item) => ({
                    item_name: item.name,
                    quantity: quantities[item.name],
                  }));

                const orderPayload = {
                  barista_ssn: currentBarista?.ssn, // Replace dynamically if needed
                  payment_method: paymentMethod,
                  order_info,
                };

                await placeOrder(orderPayload);
                setQuantities({}); // Reset quantities after successful order
                setShowModal(false);
                toast.success("Order placed successfully!");
              } catch (e) {
                toast.error("Failed to place order. Please try again.");
                console.error("Order failed", e);
              }
            }}
          />
        )}

        <footer className="footer">
          <div className="social-footer">
            <ul className="social-icons">
              <li>
                <a href="https://linkedin.com/" target="_blank">
                  LinkedIn
                </a>
              </li>
              <li>
                <a href="https://github.com/" target="_blank">
                  GitHub
                </a>
              </li>
              <li>
                <a href="https://instagram.com/" target="_blank">
                  Instagram
                </a>
              </li>
              <li>
                <a href="https://youtube.com/" target="_blank">
                  YouTube
                </a>
              </li>
            </ul>
          </div>
        </footer>
      </div>
    </>
  );
}

function capitalize(str) {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1);
}
