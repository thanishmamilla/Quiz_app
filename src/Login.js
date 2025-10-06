import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const API_BASE_URL = 'http://localhost:5000/api';

function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Use the username parsed from the token or sent by backend
        login(data.access_token, data.user_role, username); 
        onLoginSuccess();
      } else {
        alert(data.msg || "Login failed.");
      }
    } catch (error) {
      alert("Network error. Could not log in.");
    }
  };

  return (
    // ... (Login form JSX)
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
      <button type="submit">Log In</button>
    </form>
  );
}
export default Login;
// ... (Register component similar to Login)