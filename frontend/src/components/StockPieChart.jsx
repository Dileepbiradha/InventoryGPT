import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

import { Pie } from "react-chartjs-2";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

function StockPieChart({ products }) {

  if (!products || products.length === 0) {
    return <p>Loading chart...</p>;
  }

  const data = {
    labels: products.map(
      product => product.name
    ),

    datasets: [
      {
        data: products.map(
          product => product.quantity
        ),

        backgroundColor: [
          "#2563EB",
          "#DC2626",
          "#10B981",
          "#F59E0B",
          "#8B5CF6",
          "#06B6D4"
        ],

        borderColor: "#262626",
        borderWidth: 2
      }
    ]
  };

  const options = {
    responsive: true,

    plugins: {
      legend: {
        position: "bottom",

        labels: {
          color: "#F5F5F5"
        }
      }
    }
  };

  return (
    <div
      style={{
        width: "100%",
        maxWidth: "500px",
        margin: "0 auto"
      }}
    >
      <Pie
        data={data}
        options={options}
      />
    </div>
  );
}

export default StockPieChart;