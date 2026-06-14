import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";


function SalesOrders() {

  const [orders, setOrders] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);

  const [form, setForm] = useState({
    customer_id: "",
    product_id: "",
    quantity: ""
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {

    const ordersRes =
      await api.get("/sales-orders/");

    const customersRes =
      await api.get("/customers/");

    const productsRes =
      await api.get("/products/");

    setOrders(ordersRes.data);
    setCustomers(customersRes.data);
    setProducts(productsRes.data);
  };

  const handleChange = (e) => {

    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const createOrder = async (e) => {

    e.preventDefault();

    try {

      await api.post(
        "/sales-orders/",
        {
          customer_id:
            Number(form.customer_id),

          product_id:
            Number(form.product_id),

          quantity:
            Number(form.quantity)
        }
      );

      loadData();

      alert(
        "Sales Order Created"
      );

    } catch (error) {

      console.error(error);

      alert(
        "Failed to create order"
      );
    }
  };

  const approveOrder = async (id) => {

    try {

      await api.post(
        `/sales-orders/${id}/approve`
      );

      loadData();

      alert(
        "Order Approved"
      );

    } catch (error) {

      console.error(error);

      alert(
        error.response?.data?.error
      );
    }
  };

  return (
    <>
      <Navbar />

      <div style={{ padding: "30px" }}>

        <h1>Sales Orders</h1>

        <form
          onSubmit={createOrder}
          style={{
            display: "grid",
            gap: "10px",
            maxWidth: "500px"
          }}
        >

          <select
            name="customer_id"
            value={form.customer_id}
            onChange={handleChange}
            required
          >
            <option value="">
              Select Customer
            </option>

            {customers.map((c) => (
              <option
                key={c.id}
                value={c.id}
              >
                {c.name}
              </option>
            ))}
          </select>

          <select
            name="product_id"
            value={form.product_id}
            onChange={handleChange}
            required
          >
            <option value="">
              Select Product
            </option>

            {products.map((p) => (
              <option
                key={p.id}
                value={p.id}
              >
                {p.name}
              </option>
            ))}
          </select>

          <input
            type="number"
            name="quantity"
            placeholder="Quantity"
            value={form.quantity}
            onChange={handleChange}
            required
          />

          <button type="submit">
            Create Order
          </button>

        </form>

        <br />

        <table
          border="1"
          cellPadding="10"
          width="100%"
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Product</th>
              <th>Qty</th>
              <th>Status</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            {orders.map((order) => (

              <tr key={order.id}>

                <td>{order.id}</td>

                <td>
                  {order.customer_name}
                </td>

                <td>
                  {order.product_name}
                </td>

                <td>
                  {order.quantity}
                </td>

                <td>
                  {order.status}
                </td>

                <td>
                  {order.created_at}
                </td>

                <td>

                  {order.status ===
                    "Pending" && (

                    <button
                      onClick={() =>
                        approveOrder(
                          order.id
                        )
                      }
                    >
                      Approve
                    </button>

                  )}

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>
    </>
  );
}

export default SalesOrders;