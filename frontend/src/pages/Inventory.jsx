import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";


function Inventory() {

  const [products, setProducts] = useState([]);
  const [quantity, setQuantity] = useState({});

  const loadProducts = async () => {
    try {

      const response =
        await api.get("/products/");

      setProducts(response.data);

    } catch (error) {

      console.error(error);

    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

const stockIn = async (id) => {

  const qty = Number(
    quantity[id] || 0
  );

  if (qty <= 0) {
    alert("Enter valid quantity");
    return;
  }

  try {

    await api.post(
      "/inventory/stock-in",
      {
        product_id: id,
        quantity: qty
      }
    );

    await loadProducts();

    setQuantity((prev) => ({
      ...prev,
      [id]: ""
    }));

    alert(
      "Stock added successfully"
    );

  } catch (error) {

    console.error(error);

    alert(
      error?.response?.data?.error ||
      error?.message ||
      "Stock In failed"
    );
  }
};


const stockOut = async (id) => {

  const qty = Number(
    quantity[id] || 0
  );

  if (qty <= 0) {
    alert("Enter valid quantity");
    return;
  }

  try {

    await api.post(
      "/inventory/stock-out",
      {
        product_id: id,
        quantity: qty
      }
    );

    await loadProducts();

    setQuantity((prev) => ({
      ...prev,
      [id]: ""
    }));

    alert(
      "Stock removed successfully"
    );

  } catch (error) {

    console.error(error);

    alert(
      error?.response?.data?.error ||
      error?.message ||
      "Stock Out failed"
    );
  }
};

  return (
      <>
    <Navbar />
    <div style={{ padding: "30px" }}>

      <h1>Inventory Management</h1>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse"
        }}
      >
        <thead>
          <tr>
            <th>Name</th>
            <th>Current Stock</th>
            <th>Quantity</th>
            <th>Stock In</th>
            <th>Stock Out</th>
          </tr>
        </thead>

        <tbody>

          {products.map(product => (

            <tr key={product.id}>

              <td>{product.name}</td>

              <td>{product.quantity}</td>

              <td>

                <input
                  type="number"
                  value={
                    quantity[product.id] || ""
                  }
                  onChange={(e) =>
                    setQuantity({
                      ...quantity,
                      [product.id]:
                        e.target.value
                    })
                  }
                />

              </td>

              <td>

                <button
                  onClick={() =>
                    stockIn(product.id)
                  }
                >
                  + Add
                </button>

              </td>

              <td>

                <button
                  onClick={() =>
                    stockOut(product.id)
                  }
                >
                  - Remove
                </button>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
    </>
  );
}

export default Inventory;