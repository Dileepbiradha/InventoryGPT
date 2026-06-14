import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaSearch } from "react-icons/fa";
import api from "../services/api";
import Navbar from "../components/Navbar";
import StockPieChart from "../components/StockPieChart";

function Home() {
  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const res = await api.get("/products/");
      setProducts(res.data);
    } catch (error) {
      console.error("PRODUCT ERROR", error);
    }
  };

  const handleSearch = () => {
    const found = products.find((p) =>
      p.name.toLowerCase().includes(search.toLowerCase())
    );

    if (found) {
      setSelectedProduct(found);
      setMessage("");
    } else {
      setSelectedProduct(null);
      setMessage("No Product Found");
    }
  };

  return (
    <>
      <Navbar />

      <div className="home-container">
        <h1>Inventory Dashboard</h1>

        <div className="search-box">
          <input
            type="text"
            placeholder="Search Product..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <button onClick={handleSearch}>
            <FaSearch />
          </button>
        </div>

        {message && (
          <p className="error-message">
            {message}
          </p>
        )}

        <div className="chart-card">
          <h2>Inventory Distribution</h2>

          <StockPieChart products={products} />
        </div>
      </div>

      {selectedProduct && (
        <div className="modal-overlay">
          <div className="product-modal">
            <h2>{selectedProduct.name}</h2>

            <p>SKU: {selectedProduct.sku}</p>

            <p>
              Quantity: {selectedProduct.quantity}
            </p>

            <p>
              Price: ₹{selectedProduct.price}
            </p>

            <button
              onClick={() =>
                setSelectedProduct(null)
              }
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default Home;