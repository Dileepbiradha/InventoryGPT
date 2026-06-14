import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

function PurchaseOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      setLoading(true);

      console.log("Loading purchase orders...");

      const response = await api.get(
        "/purchase-orders/"
      );

      console.log(
        "Purchase Orders Response:",
        response.data
      );

      setOrders(response.data || []);

    } catch (error) {
      console.error(
        "Purchase Orders Error:",
        error
      );
    } finally {
      setLoading(false);
    }
  };

  const approveOrder = async (id) => {
    try {
      await api.post(
        `/purchase-orders/${id}/approve`
      );

      alert(
        "Purchase Order Approved"
      );

      loadOrders();

    } catch (error) {
      console.error(error);

      alert(
        error?.response?.data?.error ||
        "Approval failed"
      );
    }
  };

  return (
    <>
      <Navbar />

      <div
        style={{
          padding: "30px",
          color: "white",
          minHeight: "100vh",
          background: "#0a0a0a"
        }}
      >
        <h1
          style={{
            marginBottom: "25px"
          }}
        >
          Purchase Orders
        </h1>

        {loading ? (
          <h3>Loading...</h3>
        ) : orders.length === 0 ? (
          <h3>No Purchase Orders Found</h3>
        ) : (
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              background: "#161616",
              borderRadius: "12px",
              overflow: "hidden"
            }}
          >
            <thead>
              <tr>
                <th style={th}>ID</th>
                <th style={th}>Product</th>
                <th style={th}>Supplier</th>
                <th style={th}>Quantity</th>
                <th style={th}>Status</th>
                <th style={th}>Date</th>
                <th style={th}>Action</th>
              </tr>
            </thead>

            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td style={td}>{order.id}</td>

                  <td style={td}>
                    <strong>
                      {order.product_name}
                    </strong>
                  </td>

                  <td style={td}>
                    {order.supplier}
                  </td>

                  <td style={td}>
                    {order.quantity}
                  </td>

                  <td style={td}>
                    <span
                      style={{
                        padding: "6px 12px",
                        borderRadius: "20px",
                        color: "white",
                        background:
                          order.status === "Approved"
                            ? "#10B981"
                            : "#F59E0B"
                      }}
                    >
                      {order.status}
                    </span>
                  </td>

                  <td style={td}>
                    {new Date(
                      order.created_at
                    ).toLocaleString()}
                  </td>

                  <td style={td}>
                    {order.status ===
                      "Pending" && (
                      <button
                        onClick={() =>
                          approveOrder(order.id)
                        }
                        style={{
                          background:
                            "#10B981",
                          color: "white",
                          border: "none",
                          padding:
                            "10px 16px",
                          borderRadius:
                            "8px",
                          cursor:
                            "pointer"
                        }}
                      >
                        Approve
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}

const th = {
  border: "1px solid #333",
  padding: "12px",
  background: "#1f2937",
  textAlign: "left"
};

const td = {
  border: "1px solid #333",
  padding: "12px"
};

export default PurchaseOrders;