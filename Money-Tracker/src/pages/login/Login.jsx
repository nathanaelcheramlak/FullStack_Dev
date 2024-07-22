import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { FaLock, FaUser } from "react-icons/fa";
import "./login.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/users/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });
      const data = await response.json();
      if (data.error) {
        setErrorMessage(data.error);
        setLoading(false);
        return;
      }
      redirectToHomePage();
    } catch (error) {
      setErrorMessage("Something went wrong. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const redirectToHomePage = () => {
    // Redirect to the Home page
    navigate("/transaction");
  };

  return (
    <div className="login-main">
      <div className="login-wrapper">
        <h2 className="login-header">Login</h2>
        <hr />
        {errorMessage && <p className="error-message">{errorMessage}</p>}
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
            {loading ? "Loggin in..." : "Login"}
          </button>
        </form>

        <div className="create-account">
          <p>
            Don't have an account?{" "}
            <a href="/register" className="create">
              Create Account
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
