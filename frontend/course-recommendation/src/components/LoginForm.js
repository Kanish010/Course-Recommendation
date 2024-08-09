import React, { useState } from 'react';
import axios from 'axios';
import './LoginForm.css';

const LoginForm = ({ onLogin }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isRegistering) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/register', { username, email, password });
        if (response.data.success) {
          onLogin(response.data.user_id); // Pass user_id to onLogin
        } else {
          alert(response.data.message);
        }
      } catch (error) {
        console.error('Error registering', error);
        alert('An error occurred. Please try again.');
      }
    } else {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/login', { username, password });
        if (response.data.success) {
          onLogin(response.data.user_id); // Pass user_id to onLogin
        } else {
          alert(response.data.message);
        }
      } catch (error) {
        console.error('Error logging in', error);
        alert('An error occurred. Please try again.');
      }
    }
  };

  const toggleForm = () => {
    setIsRegistering(!isRegistering);
  };

  return (
    <div className="login-form-container">
      <div className={`card ${isRegistering ? 'flipped' : ''}`}>
        <div className="login-form front">
          <h2>Welcome Back!</h2>
          <p>Please login to your account</p>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Login</button>
          </form>
          <button className="toggle-button" onClick={toggleForm}>
            New here? Register
          </button>
        </div>
        <div className="register-form back">
          <h2>Create an Account</h2>
          <p>Please fill in the details to register</p>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Register</button>
          </form>
          <button className="toggle-button" onClick={toggleForm}>
            Already have an account? Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;