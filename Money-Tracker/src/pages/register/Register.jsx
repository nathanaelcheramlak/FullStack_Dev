import { useState } from "react";
import { FaLock, FaUser, FaEnvelope } from "react-icons/fa";
import "./register.css";

function Register() {
  // State management for form inputs
  const [fullname, setFullname] = useState("");
  const [email, setEmail] = useState("");
  const [dob, setDob] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState(false);
  const [emailError, setEmailError] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();

    // Basic validation
    if (
      !email.includes("@") ||
      !email.includes(".") ||
      email.length === 0 ||
      email.length > 50
    ) {
      // Set the error state to true
      setEmailError(true);
      return;
    }

    if (password !== confirmPassword) {
      // Set the error state to true
      setPasswordError(true);
      return;
    } else {
      setPasswordError(false);
    }
    postRegister();
  };

  const postRegister = async () => {
    const response = await fetch("http://localhost:3001/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        fullname,
        email,
        dob,
        password,
      }),
    });

    const data = await response.json();

    if (data.error) {
      console.log(data.error);
    } else {
      console.log(data);
    }
  };

  return (
    <div className="register-main">
      <div className="register-wrapper">
        <h2 className="register-header">Register</h2>

        <hr />

        <form onSubmit={handleSubmit}>
          <p className="form-text">Fullname</p>
          <div className="form">
            <input
              type="text"
              placeholder="Fullname"
              value={fullname}
              onChange={(e) => setFullname(e.target.value)}
              required
            />
            <FaUser className="icon" />
          </div>

          <p className="form-text">Email</p>
          <div className={`form ${emailError ? "error" : ""}`}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <FaEnvelope className="icon" />
          </div>

          <p className="form-text">Date of Birth</p>
          <div className="form">
            <input
              type="date"
              placeholder="Date of Birth"
              value={dob}
              onChange={(e) => setDob(e.target.value)}
              required
            />
          </div>

          <p className="form-text">Password</p>
          <div className={`form ${passwordError ? "error" : ""}`}>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <FaLock className="icon" />
          </div>

          <p className="form-text">Confirm Password</p>
          <div className={`form ${passwordError ? "error" : ""}`}>
            <input
              type="password"
              placeholder={
                passwordError ? "Passwords do not match" : "Confirm Password"
              }
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
            <FaLock className="icon" />
          </div>

          <button type="submit" className="login-button">
            Register
          </button>
        </form>

        <div className="login-account">
          <p>
            Already have an account? <a className="create">Login</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Register;
