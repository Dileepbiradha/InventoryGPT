import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

function TransactionHistory() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {
    try {
      const response = await api.get(
        "/transactions/history"
      );

      setTransactions(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
      <>
    <Navbar />
    <div style={{ padding: "30px" }}>
      <h1>Transaction History</h1>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse"
        }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Product ID</th>
            <th>Type</th>
            <th>Quantity</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          {transactions.map((t) => (
            <tr key={t.id}>
              <td>{t.id}</td>
              <td>{t.product_id}</td>
              <td>{t.transaction_type}</td>
              <td>{t.quantity}</td>
              <td>{t.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    </>
  );
}

export default TransactionHistory;