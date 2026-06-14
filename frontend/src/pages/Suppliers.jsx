import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

function Suppliers() {
  const [suppliers, setSuppliers] = useState([]);

  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    address: ""
  });

  const loadSuppliers = async () => {
    try {
      const response = await api.get(
        "/suppliers/"
      );

      setSuppliers(response.data);

    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadSuppliers();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]:
        e.target.value
    });
  };

  const createSupplier = async (e) => {
    e.preventDefault();

    try {
      await api.post(
        "/suppliers/",
        form
      );

      setForm({
        name: "",
        email: "",
        phone: "",
        address: ""
      });

      loadSuppliers();

      alert(
        "Supplier added successfully"
      );

    } catch (error) {
      console.error(error);

      alert(
        "Failed to add supplier"
      );
    }
  };

  return (
    <>
      <Navbar />

      <div style={{ padding: "30px" }}>
        <h1>Suppliers</h1>

        <form
          onSubmit={createSupplier}
          style={{
            display: "grid",
            gap: "10px",
            maxWidth: "500px",
            marginBottom: "30px"
          }}
        >
          <input
            name="name"
            placeholder="Supplier Name"
            value={form.name}
            onChange={handleChange}
            required
          />

          <input
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            required
          />

          <input
            name="phone"
            placeholder="Phone"
            value={form.phone}
            onChange={handleChange}
            required
          />

          <input
            name="address"
            placeholder="Address"
            value={form.address}
            onChange={handleChange}
            required
          />

          <button type="submit">
            Add Supplier
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
            {suppliers.map(
              (supplier) => (
                <tr key={supplier.id}>
                  <td>{supplier.id}</td>
                  <td>{supplier.name}</td>
                  <td>{supplier.email}</td>
                  <td>{supplier.phone}</td>
                  <td>{supplier.address}</td>
                </tr>
              )
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}

export default Suppliers;