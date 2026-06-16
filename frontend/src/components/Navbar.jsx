import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    // Redirect to login page/home page
    navigate("/");
  };

  const linkStyle = {
    color: "#F5F5F5",
    textDecoration: "none",
    fontWeight: "500",
    padding: "10px 14px",
    borderRadius: "8px",
    transition: "0.3s"
  };

  return (
    <nav
      style={{
        background: "#161616",
        borderBottom: "1px solid #262626",
        padding: "18px 30px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        flexWrap: "wrap",
        gap: "15px"
      }}
    >
      <h2
        style={{
          color: "#2563EB",
          margin: 0,
          fontSize: "28px",
          fontWeight: "700"
        }}
      >
        InventoryGPT
      </h2>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "10px",
          alignItems: "center"
        }}
      >
        <Link to="/home" style={linkStyle}>Home</Link>
        <Link to="/dashboard" style={linkStyle}>Dashboard</Link>
        <Link to="/products" style={linkStyle}>Products</Link>
        <Link to="/inventory" style={linkStyle}>Inventory</Link>
        <Link to="/transactions" style={linkStyle}>Transactions</Link>
        <Link to="/purchase-orders" style={linkStyle}>Purchase Orders</Link>
        <Link to="/suppliers" style={linkStyle}>Suppliers</Link>
        <Link to="/customers" style={linkStyle}>Customers</Link>
        <Link to="/sales-orders" style={linkStyle}>Sales Orders</Link>
        <Link to="/analytics" style={linkStyle}>Analytics</Link>
        <Link to="/low-stock" style={linkStyle}>Low Stock</Link>
        <Link to="/ai" style={linkStyle}>AI Assistant</Link>

        <button
          onClick={handleLogout}
          style={{
            background: "#DC2626",
            color: "white",
            border: "none",
            padding: "10px 18px",
            borderRadius: "10px",
            cursor: "pointer",
            fontWeight: "600"
          }}
        >
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;