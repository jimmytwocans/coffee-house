import React, { useState } from "react";
import "./OrderSummaryModal.css"; // Create/update this file with styled classes

export default function OrderSummaryModal({
  orderList,
  quantities,
  onClose,
  onConfirm,
}) {
  const [paymentMethod, setPaymentMethod] = useState("Cash");
  const [confirmCancel, setConfirmCancel] = useState(false);

  const total = orderList.reduce(
    (sum, item) => sum + item.price * (quantities[item.name] || 0),
    0
  );

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h2>Order Summary</h2>

        <table className="summary-table">
          <thead>
            <tr>
              <th>Item</th>
              <th>Qty</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {orderList.map((item) => (
              <tr key={item.name}>
                <td>{item.name}</td>
                <td>{quantities[item.name]}</td>
                <td>${(item.price * quantities[item.name]).toFixed(2)}</td>
              </tr>
            ))}
            <tr>
              <td colSpan="2">
                <strong>Total</strong>
              </td>
              <td>
                <strong>${total.toFixed(2)}</strong>
              </td>
            </tr>
          </tbody>
        </table>

        <div className="payment-method">
          <label>Payment Method:</label>
          <select
            value={paymentMethod}
            onChange={(e) => setPaymentMethod(e.target.value)}
          >
            <option>Cash</option>
            <option>Credit Card</option>
            <option>Debit Card</option>
          </select>
        </div>

        <div className="modal-actions">
          <button
            className="confirm-btn"
            onClick={() => onConfirm(paymentMethod)}
          >
            Confirm Order
          </button>

          {!confirmCancel ? (
            <button
              className="cancel-btn"
              onClick={() => setConfirmCancel(true)}
            >
              Cancel
            </button>
          ) : (
            <div className="confirm-cancel">
              <p>Are you sure you want to cancel?</p>
              <button className="yes-btn" onClick={onClose}>
                Yes
              </button>
              <button
                className="no-btn"
                onClick={() => setConfirmCancel(false)}
              >
                No
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
