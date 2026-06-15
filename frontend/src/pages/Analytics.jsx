import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Analytics() {
  const [data, setData] = useState(null);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const response = await api.get(
        "/analytics/"
      );

      console.log(response.data);

      setData(response.data);
    } catch (error) {
      console.error(
        "Analytics Error:",
        error
      );
    }
  };

  if (!data) {
    return (
      <>
        <Navbar />
        <div style={{ padding: "30px" }}>
          <h2>Loading...</h2>
        </div>
      </>
    );
  }

  const chartData = {
    labels:
      data.top_selling?.map(
        (item) => item.name
      ) || [],

    datasets: [
      {
        label: "Units Sold",

        data:
          data.top_selling?.map(
            (item) => item.quantity
          ) || [],

        backgroundColor:
          "rgba(54,162,235,0.6)"
      }
    ]
  };

  return (
    <>
      <Navbar />

      <div style={{ padding: "30px" }}>
        <h1>Analytics</h1>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(5,1fr)",
            gap: "20px",
            marginBottom: "40px"
          }}
        >
          <div className="card">
            <h3>Products</h3>
            <h2>{data.total_products}</h2>
          </div>

          <div className="card">
            <h3>Transactions</h3>
            <h2>{data.transaction_count}</h2>
          </div>

          <div className="card">
            <h3>Low Stock</h3>
            <h2>{data.low_stock_count}</h2>
          </div>

          <div className="card">
            <h3>Inventory Value</h3>
            <h2>₹{data.inventory_value}</h2>
          </div>

          <div className="card">
            <h3>Total Revenue</h3>
            <h2>₹{data.total_revenue}</h2>
          </div>
        </div>

        <h2>Top Stock Product</h2>

        <div
          style={{
            border: "1px solid gray",
            padding: "20px",
            marginTop: "10px",
            marginBottom: "40px",
            width: "350px"
          }}
        >
          <p>
            <strong>Name:</strong>{" "}
            {data.top_stock_product?.name}
          </p>

          <p>
            <strong>Quantity:</strong>{" "}
            {data.top_stock_product?.quantity}
          </p>

          <p>
            <strong>Category:</strong>{" "}
            {data.top_stock_product?.category}
          </p>
        </div>

        <h2 style={{ marginTop: "50px" }}>
          Top Selling Products
        </h2>

        <div
          style={{
            width: "700px",
            marginTop: "20px"
          }}
        >
          <Bar data={chartData} />
        </div>
      </div>
    </>
  );
}

export default Analytics;