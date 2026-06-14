import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";

function Products() {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [search, setSearch] = useState("");
  const [editingId, setEditingId] = useState(null);

  const [form, setForm] = useState({
    name: "",
    sku: "",
    category: "",
    quantity: "",
    price: "",
    supplier: "",
  });

  const resetForm = () => {
    setForm({
      name: "",
      sku: "",
      category: "",
      quantity: "",
      price: "",
      supplier: "",
    });

    setEditingId(null);
  };

  const loadProducts = async () => {
  try {
    setLoading(true);

    const response = await api.get("/products/");

    setProducts(response.data);
    setFilteredProducts(response.data);

    setError("");

  } catch (err) {
    console.error(err);

    if (
      err?.response?.status === 401 ||
      err?.response?.status === 403
    ) {
      localStorage.clear();
      navigate("/login");
      return;
    }

    setError(
      err?.response?.data?.msg ||
      err?.response?.data?.message ||
      "Failed to load products"
    );
  } finally {
    setLoading(false);
  }
};

  const navigate = useNavigate();

useEffect(() => {
  const token = localStorage.getItem("token");

  if (!token) {
    navigate("/login");
    return;
  }

  loadProducts();
}, [navigate]);

  useEffect(() => {
    const filtered = products.filter((product) =>
      product.name.toLowerCase().includes(search.toLowerCase())
    );

    setFilteredProducts(filtered);
  }, [search, products]);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const createProduct = async (e) => {
    e.preventDefault();

    try {
      await api.post("/products/", {
        ...form,
        quantity: Number(form.quantity),
        price: Number(form.price),
      });

      resetForm();
      loadProducts();

      alert("Product created successfully");
    } catch (err) {
      console.error(err);

      alert(
        JSON.stringify(err.response?.data, null, 2) ||
          "Failed to create product"
      );
    }
  };

  const updateProduct = async (e) => {
    e.preventDefault();

    try {
      await api.put(`/products/${editingId}`, {
        ...form,
        quantity: Number(form.quantity),
        price: Number(form.price),
      });

      resetForm();
      loadProducts();

      alert("Product updated successfully");
    } catch (error) {
      console.error(error);
      alert("Update failed");
    }
  };

  const deleteProduct = async (id) => {
    const confirmDelete = window.confirm(
      "Delete this product?"
    );

    if (!confirmDelete) return;

    try {
      await api.delete(`/products/${id}`);

      loadProducts();

      alert("Product deleted successfully");
    } catch (error) {
      console.error(error);
      alert("Delete failed");
    }
  };

  const editProduct = (product) => {
    setEditingId(product.id);

    setForm({
      name: product.name,
      sku: product.sku,
      category: product.category,
      quantity: product.quantity,
      price: product.price,
      supplier: product.supplier,
    });

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const stockIn = async (id) => {
  const qty = prompt(
    "Enter quantity to add:"
  );

  if (!qty || Number(qty) <= 0) {
    return;
  }

  try {
    await api.post(
      "/inventory/stock-in",
      {
        product_id: id,
        quantity: Number(qty),
      }
    );

    await loadProducts();

    alert(
      "Stock added successfully"
    );

  } catch (error) {
    console.error(error);

    alert(
      error?.response?.data?.error ||
      error?.response?.data?.msg ||
      error?.message ||
      "Stock In failed"
    );
  }
};


  const stockOut = async (id) => {
  const qty = prompt(
    "Enter quantity to remove:"
  );

  if (!qty || Number(qty) <= 0) {
    return;
  }

  try {
    await api.post(
      "/inventory/stock-out",
      {
        product_id: id,
        quantity: Number(qty),
      }
    );

    await loadProducts();

    alert(
      "Stock removed successfully"
    );

  } catch (error) {
    console.error(error);

    alert(
      error?.response?.data?.error ||
      error?.response?.data?.msg ||
      error?.message ||
      "Stock Out failed"
    );
  }
};

  return (
      <>
    <Navbar />
    <div style={{ padding: "30px" }}>
      <h1>Products</h1>

      <div
        style={{
          background: "#1f2937",
          padding: "20px",
          borderRadius: "10px",
          marginBottom: "20px",
        }}
      >
        <h3>Total Products: {products.length}</h3>

        <h3>
          Inventory Value: ₹
          {products.reduce(
            (sum, p) => sum + p.price * p.quantity,
            0
          )}
        </h3>
      </div>

      <input
        type="text"
        placeholder="Search products..."
        value={search}
        onChange={(e) =>
          setSearch(e.target.value)
        }
        style={{
          padding: "10px",
          width: "300px",
          marginBottom: "20px",
        }}
      />

      <form
        onSubmit={
          editingId
            ? updateProduct
            : createProduct
        }
        style={{
          display: "grid",
          gap: "10px",
          marginBottom: "30px",
          maxWidth: "500px",
        }}
      >
        <input
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
          required
        />

        <input
          name="sku"
          placeholder="SKU"
          value={form.sku}
          onChange={handleChange}
          required
        />

        <input
          name="category"
          placeholder="Category"
          value={form.category}
          onChange={handleChange}
          required
        />

        <input
          name="quantity"
          type="number"
          placeholder="Quantity"
          value={form.quantity}
          onChange={handleChange}
          required
        />

        <input
          name="price"
          type="number"
          placeholder="Price"
          value={form.price}
          onChange={handleChange}
          required
        />

        <input
          name="supplier"
          placeholder="Supplier"
          value={form.supplier}
          onChange={handleChange}
          required
        />

        <button type="submit">
          {editingId
            ? "Update Product"
            : "Add Product"}
        </button>

        {editingId && (
          <button
            type="button"
            onClick={resetForm}
          >
            Cancel Edit
          </button>
        )}
      </form>

      {loading && <p>Loading...</p>}

      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}

      {!loading &&
        filteredProducts.length === 0 && (
          <p>No products found.</p>
        )}

      {filteredProducts.length > 0 && (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
          }}
        >
          <thead>
            <tr>
              <th>Name</th>
              <th>SKU</th>
              <th>Category</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Supplier</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {filteredProducts.map((product) => (
              <tr key={product.id}>
                <td>{product.name}</td>
                <td>{product.sku}</td>
                <td>{product.category}</td>
                <td>{product.quantity}</td>
                <td>₹ {product.price}</td>
                <td>{product.supplier}</td>

                <td>
                  <button
                    onClick={() =>
                      editProduct(product)
                    }
                  >
                    Edit
                  </button>

                  <button
                    onClick={() =>
                      deleteProduct(product.id)
                    }
                    style={{
                      marginLeft: "10px",
                      background: "red",
                      color: "white",
                    }}
                  >
                    Delete
                  </button>

                  <button
                    onClick={() =>
                      stockIn(product.id)
                    }
                    style={{
                      marginLeft: "5px",
                      background: "green",
                      color: "white",
                    }}
                  >
                    Stock In
                  </button>

                  <button
                    onClick={() =>
                      stockOut(product.id)
                    }
                    style={{
                      marginLeft: "5px",
                      background: "orange",
                      color: "white",
                    }}
                  >
                    Stock Out
                  </button>
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

export default Products;