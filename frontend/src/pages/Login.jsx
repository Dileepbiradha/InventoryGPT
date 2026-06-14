import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError("");

      const data = await loginUser(
        email,
        password
      );

      console.log(
        "LOGIN RESPONSE:",
        data
      );

      // Support different token names
      const token =
        data?.access_token ||
        data?.token ||
        data?.jwt;

      if (!token) {
        throw new Error(
          "No token returned from server"
        );
      }

      // Save token
      localStorage.setItem(
        "token",
        token
      );

      // Save user if returned
      if (data?.user) {
        localStorage.setItem(
          "user",
          JSON.stringify(data.user)
        );
      }

      console.log(
        "Stored Token:",
        localStorage.getItem("token")
      );

      alert("Login successful");

      // Redirect to Home Page
      navigate("/home");

    } catch (err) {
      console.error(
        "LOGIN ERROR:",
        err
      );

      setError(
        err?.response?.data?.msg ||
        err?.response?.data?.message ||
        err?.response?.data?.error ||
        err?.message ||
        "Invalid credentials"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#111827",
      }}
    >
      <div
        style={{
          background: "#1f2937",
          padding: "30px",
          borderRadius: "10px",
          width: "350px",
        }}
      >
        <h1
          style={{
            color: "white",
            textAlign: "center",
            marginBottom: "20px",
          }}
        >
          InventoryGPT Login
        </h1>

        {error && (
          <p
            style={{
              color: "red",
              marginBottom: "15px",
            }}
          >
            {error}
          </p>
        )}

        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            required
            autoComplete="email"
            style={{
              width: "100%",
              padding: "12px",
              marginBottom: "15px",
              boxSizing: "border-box",
            }}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            required
            autoComplete="current-password"
            style={{
              width: "100%",
              padding: "12px",
              marginBottom: "15px",
              boxSizing: "border-box",
            }}
          />

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "12px",
              cursor: "pointer",
              background: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "5px",
            }}
          >
            {loading
              ? "Logging in..."
              : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;