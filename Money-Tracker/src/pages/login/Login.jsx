import { useState } from "react";
import { FaLock, FaUser } from "react-icons/fa";
import "./login.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch("https://localhost:5000", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const result = await response.json();
      console.log("Login successful:", result);
      // Handle success (e.g., navigate to another page or show a success message)
    } catch (error) {
      console.error("Login failed:", error);
      // Handle error (e.g., show an error message)
    }
  };

  return (
    <div className="login-main">
      <div className="login-wrapper">
        <h2 className="login-header">Login</h2>
        <hr />
        <form onSubmit={handleSubmit}>
          <div className="form">
            <input
              type="text"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <FaUser className="icon" />
          </div>

          <div className="form">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <FaLock className="icon" />
          </div>

          <button type="submit" className="login-button">
            Login
          </button>
        </form>

        <div className="create-account">
          <p>
            Don't have an account? <a className="create">Create Account</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
