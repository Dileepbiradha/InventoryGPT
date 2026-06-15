import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

import { Bar, Pie } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function Dashboard() {
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    loadDashboard();
    loadAnalytics();
  }, []);

  const loadDashboard = async () => {
    try {
      const response = await fetch(
        "https://inventorygpt.onrender.com/api/dashboard/"
      );

      if (!response.ok) {
        throw new Error("Failed to load dashboard");
      }

      const result = await response.json();

      console.log("Dashboard:", result);

      setData(result);
    } catch (error) {
      console.error("Dashboard Error:", error);
    }
  };

  const loadAnalytics = async () => {
    try {
      const response = await fetch(
        "https://inventorygpt.onrender.com/api/analytics/"
      );

      if (!response.ok) {
        throw new Error("Failed to load analytics");
      }

      const result = await response.json();

      console.log("Analytics:", result);

      setAnalytics(result);
    } catch (error) {
      console.error("Analytics Error:", error);
    }
  };

    const downloadReport = () => {
      window.open(
        "https://inventorygpt.onrender.com/api/reports/inventory",
        "_blank"
      );
    };

  if (!data || !analytics) {
    return (
      <>
        <Navbar />

        <div
          style={{
            minHeight: "100vh",
            background: "#0A0A0A",
            color: "#F5F5F5",
            padding: "40px"
          }}
        >
          <h2>Loading Dashboard...</h2>
        </div>
      </>
    );
  }

  const stockChartData = {
    labels: data.products.map((product) => product.name),

    datasets: [
      {
        label: "Stock Quantity",
        data: data.products.map(
          (product) => product.quantity
        ),
        backgroundColor: "#2563EB",
        borderRadius: 8
      }
    ]
  };

  const pieChartData = {
    labels: [
      "Products",
      "Transactions",
      "Low Stock"
    ],

    datasets: [
      {
        data: [
          analytics.total_products,
          analytics.transaction_count,
          analytics.low_stock_count
        ],

        backgroundColor: [
          "#2563EB",
          "#10B981",
          "#DC2626"
        ]
      }
    ]
  };

  return (
    <>
      <Navbar />

      <div
        style={{
          padding: "30px",
          background: "#0A0A0A",
          minHeight: "100vh",
          color: "#F5F5F5"
        }}
      >
        <h1>Inventory Dashboard</h1>

        <button
          onClick={downloadReport}
          style={{
            background: "#2563EB",
            color: "white",
            border: "none",
            padding: "12px 20px",
            borderRadius: "10px",
            marginBottom: "30px",
            cursor: "pointer"
          }}
        >
          Download Inventory Report
        </button>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit,minmax(220px,1fr))",
            gap: "20px",
            marginBottom: "30px"
          }}
        >
          <div className="card">
            <h4>Total Products</h4>
            <h2>{analytics.total_products}</h2>
          </div>

          <div className="card">
            <h4>Transactions</h4>
            <h2>{analytics.transaction_count}</h2>
          </div>

          <div className="card">
            <h4>Low Stock</h4>
            <h2 style={{ color: "#DC2626" }}>
              {analytics.low_stock_count}
            </h2>
          </div>

          <div className="card">
            <h4>Inventory Value</h4>
            <h2>₹{analytics.inventory_value}</h2>
          </div>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "25px",
            marginBottom: "40px"
          }}
        >
          <div className="card">
            <h3>Inventory Stock Levels</h3>
            <Bar data={stockChartData} />
          </div>

          <div className="card">
            <h3>Inventory Overview</h3>
            <Pie data={pieChartData} />
          </div>
        </div>

        <div className="card">
          <h2>Low Stock Alerts</h2>

          {data.low_stock.length === 0 ? (
            <p>No low stock products</p>
          ) : (
            data.low_stock.map((product) => (
              <p
                key={product.id}
                style={{ color: "#DC2626" }}
              >
                {product.name} ({product.quantity})
              </p>
            ))
          )}
        </div>

        <div className="card">
          <h2>Recent Transactions</h2>

          <table
            style={{
              width: "100%",
              borderCollapse: "collapse"
            }}
          >
            <thead>
              <tr>
                <th>ID</th>
                <th>Product</th>
                <th>Type</th>
                <th>Quantity</th>
                <th>Date</th>
              </tr>
            </thead>

            <tbody>
              {data.recent_transactions.map(
                (transaction) => (
                  <tr key={transaction.id}>
                    <td>{transaction.id}</td>
                    <td>{transaction.product_id}</td>
                    <td>
                      {transaction.transaction_type}
                    </td>
                    <td>{transaction.quantity}</td>
                    <td>{transaction.created_at}</td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

export default Dashboard;