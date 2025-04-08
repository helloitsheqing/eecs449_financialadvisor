import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';
import LogUserContext from './context.js';

const LoginPage = () => {
    const navigate = useNavigate();
    const {setUsername} = useContext(LogUserContext);
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(''); // Clear previous errors

        // Basic validation
        if (!formData.username || !formData.password) {
            setError('Please fill in all fields');
            return;
        }

        try {
            const response = await fetch('http://localhost:5001/auth/login', {
                method: 'POST',
                credentials: "include",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                // Store the authentication token if your backend returns one
                if (data.token) {
                    localStorage.setItem('authToken', data.token);
                }
                setUsername(formData.username);
                navigate('/chat');
            } else {
                setError(data.message || 'Login failed');
            }
        } catch (err) {
            setError('An error occurred. Please try again.');
            console.error('Login error:', err);
        }
    };

    return (
        <div className="container">
            <h1>Laughing Stocks</h1>
            <h2>Your Financial Advisor for Less Stress and More Success</h2>
            
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input 
                        type="text" 
                        id="username" 
                        name="username" 
                        value={formData.username}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input 
                        type="password" 
                        id="password" 
                        name="password" 
                        value={formData.password}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                {error && <div className="error-message">{error}</div>}
                <div className="form-group">
                    <button type="submit">Login</button>
                </div>
            </form>
        </div>
    );
};

export default LoginPage; // Fixed export name (was exporting HomePage)
