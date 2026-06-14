import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

function Customers() {

  const [customers, setCustomers] = useState([]);

  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    address: ""
  });

  const loadCustomers = async () => {
    try {

      const response =
        await api.get("/customers/");

      setCustomers(response.data);

    } catch (error) {

      console.error(error);

      alert("Failed to load customers");
    }
  };

  useEffect(() => {
    loadCustomers();
  }, []);

  const handleChange = (e) => {

    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const createCustomer = async (e) => {

    e.preventDefault();

    try {

      await api.post(
        "/customers/",
        form
      );

      setForm({
        name: "",
        email: "",
        phone: "",
        address: ""
      });

      loadCustomers();

      alert(
        "Customer added successfully"
      );

    } catch (error) {

      console.error(error);

      alert(
        "Failed to create customer"
      );
    }
  };

  return (
    <>
      <Navbar />

      <div style={{ padding: "30px" }}>

        <h1>Customers</h1>

        <form
          onSubmit={createCustomer}
          style={{
            maxWidth: "500px",
            marginBottom: "30px",
            display: "grid",
            gap: "10px"
          }}
        >

          <input
            name="name"
            placeholder="Customer Name"
            value={form.name}
            onChange={handleChange}
            required
          />

          <input
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
          />

          <input
            name="phone"
            placeholder="Phone"
            value={form.phone}
            onChange={handleChange}
          />

          <input
            name="address"
            placeholder="Address"
            value={form.address}
            onChange={handleChange}
          />

          <button type="submit">
            Add Customer
          </button>

        </form>

        <table
          border="1"
          cellPadding="10"
          width="100%"
        >

          <thead>

            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Address</th>
            </tr>

          </thead>

          <tbody>

            {customers.map(
              (customer) => (
                <tr key={customer.id}>
                  <td>{customer.id}</td>
                  <td>{customer.name}</td>
                  <td>{customer.email}</td>
                  <td>{customer.phone}</td>
                  <td>{customer.address}</td>
                </tr>
              )
            )}

          </tbody>

        </table>

      </div>
    </>
  );
}

export default Customers;