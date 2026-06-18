import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

function PurchaseOrders() {
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    product_id: "",
    quantity: "",
    supplier: ""
  });

  useEffect(() => {
    loadOrders();
    loadProducts();
  }, []);

  const loadOrders = async () => {
    try {
      setLoading(true);
      const response = await api.get("/purchase-orders/");
      setOrders(response.data || []);
    } catch (error) {
      console.error("Purchase Orders Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadProducts = async () => {
    try {
      const response = await api.get("/products/");
      setProducts(response.data || []);
    } catch (error) {
      console.error("Products Error:", error);
    }
  };

  const createOrder = async (e) => {
    e.preventDefault();
    try {
      await api.post("/purchase-orders/", {
        product_id: parseInt(form.product_id),
        quantity: parseInt(form.quantity),
        supplier: form.supplier
      });
      alert("Purchase Order Created");
      setShowForm(false);
      setForm({ product_id: "", quantity: "", supplier: "" });
      loadOrders();
    } catch (error) {
      alert(error?.response?.data?.error || "Create failed");
    }
  };

  const approveOrder = async (id) => {
    try {
      await api.post(`/purchase-orders/${id}/approve`);
      alert("Purchase Order Approved");
      loadOrders();
    } catch (error) {
      alert(error?.response?.data?.error || "Approval failed");
    }
  };

  return (
    <>
      <Navbar />
      <div style={{ padding: "30px", color: "white", minHeight: "100vh", background: "#0a0a0a" }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "25px" }}>
          <h1>Purchase Orders</h1>
          <button
            onClick={() => setShowForm(!showForm)}
            style={{
              background: "#3B82F6",
              color: "white",
              border: "none",
              padding: "10px 20px",
              borderRadius: "8px",
              cursor: "pointer"
            }}
          >
            {showForm ? "Cancel" : "+ New Purchase Order"}
          </button>
        </div>

        {showForm && (
          <form
            onSubmit={createOrder}
            style={{
              background: "#161616",
              padding: "20px",
              borderRadius: "12px",
              marginBottom: "20px",
              display: "flex",
              gap: "10px",
              flexWrap: "wrap"
            }}
          >
            <select
              required
              value={form.product_id}
              onChange={(e) => setForm({ ...form, product_id: e.target.value })}
              style={inputStyle}
            >
              <option value="">Select Product</option>
              {products.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>

            <input
              type="number"
              placeholder="Quantity"
              required
              min="1"
              value={form.quantity}
              onChange={(e) => setForm({ ...form, quantity: e.target.value })}
              style={inputStyle}
            />

            <input
              type="text"
              placeholder="Supplier"
              required
              value={form.supplier}
              onChange={(e) => setForm({ ...form, supplier: e.target.value })}
              style={inputStyle}
            />

            <button
              type="submit"
              style={{
                background: "#10B981",
                color: "white",
                border: "none",
                padding: "10px 20px",
                borderRadius: "8px",
                cursor: "pointer"
              }}
            >
              Create
            </button>
          </form>
        )}

        {loading ? (
          <h3>Loading...</h3>
        ) : orders.length === 0 ? (
          <h3>No Purchase Orders Found</h3>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse", background: "#161616", borderRadius: "12px", overflow: "hidden" }}>
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
                  <td style={td}><strong>{order.product_name}</strong></td>
                  <td style={td}>{order.supplier}</td>
                  <td style={td}>{order.quantity}</td>
                  <td style={td}>
                    <span style={{
                      padding: "6px 12px",
                      borderRadius: "20px",
                      color: "white",
                      background: order.status === "Approved" ? "#10B981" : "#F59E0B"
                    }}>
                      {order.status}
                    </span>
                  </td>
                  <td style={td}>{new Date(order.created_at).toLocaleString()}</td>
                  <td style={td}>
                    {order.status === "Pending" && (
                      <button
                        onClick={() => approveOrder(order.id)}
                        style={{
                          background: "#10B981",
                          color: "white",
                          border: "none",
                          padding: "10px 16px",
                          borderRadius: "8px",
                          cursor: "pointer"
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

const th = { border: "1px solid #333", padding: "12px", background: "#1f2937", textAlign: "left" };
const td = { border: "1px solid #333", padding: "12px" };
const inputStyle = {
  padding: "10px",
  borderRadius: "8px",
  border: "1px solid #333",
  background: "#0a0a0a",
  color: "white",
  minWidth: "180px"
};

export default PurchaseOrders;