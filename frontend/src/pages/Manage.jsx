import React, { useState, useEffect } from "react";
import {
  fetchManagers,
  fetchBaristas,
  addBarista,
  deleteBarista,
    fetchInventory,
    placeRefillOrder,
} 
from "../api/api";
import "./Manage.css";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

export default function Manage() {
  const [managers, setManagers] = useState([]);
  const [baristas, setBaristas] = useState([]);
  const [newBarista, setNewBarista] = useState({
    ssn: "",
    name: "",
    email: "",
    salary: "",
    start_time: "",
    end_time: "",
    days_working: [],
  });
  const [inventory, setInventory] = useState([]);
  const [refillData, setRefillData] = useState({});

  const navigate = useNavigate();
  useEffect(() => {
    loadManagers();
    loadBaristas();
    loadInventory();
  }, []);

  const activeManagerSSN = "123-45-6789"; // Alice's SSN

  const loadInventory = async () => {
    try {
      const data = await fetchInventory();
      setInventory(data);
    } catch (err) {
      console.error("Failed to fetch inventory", err);
    }
  };

  const loadManagers = async () => {
    try {
      const data = await fetchManagers();
      setManagers(data);
    } catch (err) {
      console.error("Failed to fetch managers", err);
    }
  };


  const handleRefillSubmit = async (itemName) => {
    const quantity = parseInt(refillData[itemName], 10);

    if (isNaN(quantity) || quantity <= 0) {
      toast.error("Please enter a valid quantity.");
      return;
    }

    const payload = {
      manager_ssn: activeManagerSSN,
      item_name: itemName,
      quantity,
    };

    try {
      const result = await placeRefillOrder(payload); // use result for feedback/logs
      console.log(`Refill success:`, result); // optional

      toast.success(`Refill placed for ${itemName} (Qty: ${quantity})`);
      setRefillData((prev) => ({ ...prev, [itemName]: "" }));
      await loadInventory(); // update stock shown in UI
    } catch (err) {
      const message =
        err.response?.statusText ||
        err.message ||
        "Unknown error occurred during refill.";
      toast.error(`Error refilling ${itemName}: ${message}`);
      console.error("Refill error:", err);
    }
  };





  const loadBaristas = async () => {
    try {
      const data = await fetchBaristas();
      setBaristas(data);
    } catch (err) {
      console.error("Failed to fetch baristas", err);
    }
  };

  const handleRefillChange = (name, value) => {
    setRefillData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleBaristaChange = (e) => {
    const { name, value, checked } = e.target;

    if (name == "days_working") {
      setNewBarista((prev) => {
        const updateDays = new Set(prev.days_working);
        checked ? updateDays.add(value) : updateDays.delete(value);
        return {
          ...prev,
          days_working: Array.from(updateDays),
        };
      });
    } else {
      setNewBarista((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const handleAddBarista = async (e) => {
    e.preventDefault();
    try {
      await addBarista(newBarista);
      await loadBaristas();
      toast.success("Barista added successfully!");
      setNewBarista({
        ssn: "",
        name: "",
        age: "",
        email: "",
        salary: "",
        experience: "",
        start_time: "",
        end_time: "",
        days_working: [],
      });

    } catch (err) {
      toast.error("Failed to add barista. Please check the details. "+err.message);
      console.error("Error adding barista:", err);
    }
  };

  const handleDeleteBarista = async (ssn) => {
    try {
      await deleteBarista(ssn);
      await loadBaristas();
      toast.success("Barista deleted successfully!");
    } catch (err) {
      toast.error("Failed to delete barista. Please try again."+err.message);
      console.error("Error deleting barista:", err);
    }
  };

  return (
    <div className="manage-container">
      <header className="navbar">
        <span onClick={() => navigate("/")} style={{ cursor: "pointer" }}>
          CoffeeHouse
        </span>
      </header>

      <main className="content">
        <h1>Manage</h1>
        <p className="subtitle">
          Your beloved servers, Delivering your best coffees.
        </p>

        {/* Managers Table */}
        <h2>Managers</h2>
        <table className="centered-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Ownership (%)</th>
            </tr>
          </thead>
          <tbody>
            {managers.map((manager) => (
              <tr key={manager.ssn}>
                <td
                  style={{ display: "flex", alignItems: "center", gap: "8px" }}
                >
                  {manager.name}
                  {manager.ssn === activeManagerSSN && (
                    <span
                      style={{
                        width: "10px",
                        height: "10px",
                        backgroundColor: "green",
                        borderRadius: "50%",
                        display: "inline-block",
                      }}
                      title="Active Manager"
                    ></span>
                  )}
                </td>
                <td>{manager.ownership}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Baristas Section */}
        <h2 style={{ marginTop: "40px" }}>Baristas</h2>
        <table className="centered-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>SSN</th>
              <th>Email</th>
              <th>Salary</th>
              <th>Days Working</th>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {baristas.map((barista) => (
              <tr key={barista.ssn}>
                <td>{barista.name}</td>
                <td>{barista.ssn}</td>
                <td>{barista.email}</td>
                <td>{barista.salary}</td>
                <td>
                  {Array.isArray(barista.days_working)
                    ? barista.days_working.join(", ")
                    : "N/A"}
                </td>
                <td>{barista.start_time}</td>
                <td>{barista.end_time}</td>
                <td>
                  <button
                    onClick={() => handleDeleteBarista(barista.ssn)}
                    className="delete-btn"
                  >
                    Remove Barista
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <br />

        {/* Add Barista Form */}
        <form onSubmit={handleAddBarista} className="add-form">
          <h3>Add New Barista</h3>
          <input
            type="text"
            name="ssn"
            placeholder="SSN (e.g., 123-45-6789)"
            value={newBarista.ssn}
            onChange={handleBaristaChange}
            required
          />
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={newBarista.name}
            onChange={handleBaristaChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={newBarista.email}
            onChange={handleBaristaChange}
            required
          />
          <input
            type="number"
            name="salary"
            placeholder="Annual Salary"
            value={newBarista.salary}
            onChange={handleBaristaChange}
            required
          />
          <input
            type="time"
            name="start_time"
            value={newBarista.start_time}
            onChange={handleBaristaChange}
            required
          />
          <input
            type="time"
            name="end_time"
            value={newBarista.end_time}
            onChange={handleBaristaChange}
            required
          />
          <div className="day-checkboxes">
            <legend>Days Working</legend>
            <div className="checkbox-container">
              {[
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
              ].map((day) => (
                <label key={day} className="checkbox-label">
                  <input
                    type="checkbox"
                    name="days_working"
                    value={day}
                    checked={newBarista.days_working.includes(day)}
                    onChange={handleBaristaChange}
                  />
                  <span>{day}</span>
                </label>
              ))}
            </div>
          </div>
          <button type="submit" className="add-btn">
            Add Barista
          </button>
        </form>

        <h1 style={{ marginTop: "40px" }}>Inventory Restock</h1>
        <table className="centered-table">
          <thead>
            <tr>
              <th>Inventory Name</th>
              <th>Price per Unit</th>
              <th>Remaning Stock</th>
              <th>Quantity</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {inventory.map((item) => (
              <tr key={item.name}>
                <td>{item.name}</td>
                <td>{item.price}</td>
                <td>{item.stock_quantity}</td>
                <td>
                  <input
                    type="number"
                    min="1"
                    placeholder={`Qty (${item.unit})`}
                    value={refillData[item.name] || ""}
                    onChange={(e) =>
                      handleRefillChange(item.name, e.target.value)
                    }
                  />
                </td>
                <td>
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                        handleRefillSubmit(item.name)
                    } }//
                    className="refil-btn"
                  >
                    Place Refil
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}
