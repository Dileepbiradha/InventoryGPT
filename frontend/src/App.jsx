import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import Login from "./pages/Login";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Products from "./pages/Products";
import Inventory from "./pages/Inventory";
import Transactions from "./pages/Transactions";
import PurchaseOrders from "./pages/PurchaseOrders";
import Suppliers from "./pages/Suppliers";
import Customers from "./pages/Customers";
import Analytics from "./pages/Analytics";
import LowStock from "./pages/LowStock";
import AIChat from "./pages/AIChat";
import SalesOrders from "./pages/SalesOrders";

/*
  PROTECTED ROUTE
*/
function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* LOGIN */}

        <Route
          path="/login"
          element={<Login />}
        />

        {/* ROOT REDIRECT */}

        <Route
          path="/"
          element={
            localStorage.getItem("token")
              ? <Navigate to="/home" replace />
              : <Navigate to="/login" replace />
          }
        />

        {/* HOME */}

        <Route
          path="/home"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />

        {/* DASHBOARD */}

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* PRODUCTS */}

        <Route
          path="/products"
          element={
            <ProtectedRoute>
              <Products />
            </ProtectedRoute>
          }
        />

        {/* INVENTORY */}

        <Route
          path="/inventory"
          element={
            <ProtectedRoute>
              <Inventory />
            </ProtectedRoute>
          }
        />

        {/* TRANSACTIONS */}

        <Route
          path="/transactions"
          element={
            <ProtectedRoute>
              <Transactions />
            </ProtectedRoute>
          }
        />

        {/* PURCHASE ORDERS */}

        <Route
          path="/purchase-orders"
          element={
            <ProtectedRoute>
              <PurchaseOrders />
            </ProtectedRoute>
          }
        />

        {/* SUPPLIERS */}

        <Route
          path="/suppliers"
          element={
            <ProtectedRoute>
              <Suppliers />
            </ProtectedRoute>
          }
        />

        {/* CUSTOMERS */}

        <Route
          path="/customers"
          element={
            <ProtectedRoute>
              <Customers />
            </ProtectedRoute>
          }
        />

        {/* ANALYTICS */}

        <Route
          path="/analytics"
          element={
            <ProtectedRoute>
              <Analytics />
            </ProtectedRoute>
          }
        />

        {/* LOW STOCK */}

        <Route
          path="/low-stock"
          element={
            <ProtectedRoute>
              <LowStock />
            </ProtectedRoute>
          }
        />

        {/* AI CHAT */}

        <Route
          path="/ai-chat"
          element={
            <ProtectedRoute>
              <AIChat />
            </ProtectedRoute>
          }
        />

        {/* SALES ORDERS */}

        <Route
          path="/sales-orders"
          element={
            <ProtectedRoute>
              <SalesOrders />
            </ProtectedRoute>
          }
        />

        {/* UNKNOWN ROUTES */}

        <Route
          path="*"
          element={
            <Navigate
              to="/home"
              replace
            />
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;