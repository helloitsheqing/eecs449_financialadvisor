// this file needs more work because right now it is just a copy of the login page

import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';
// import React from 'react';
import LogUserContext from './contexts/context.js';

const SignupPage = () => {
    const navigate = useNavigate();
    const { setUsername } = useContext(LogUserContext);
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
            const response = await fetch('http://localhost:5001/auth/signup', {
                method: 'POST',
                credentials: "include",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            console.log("response: ", response)

            const data = await response.json();

            if (response.ok) {
                // Store the authentication token if your backend returns one
                if (data.token) {
                    localStorage.setItem('authToken', data.token);
                }
                setUsername(formData.username);
                navigate('/chat');
            } else {
                setError(data.message || 'Signup failed');
            }
        } catch (err) {
            setError('An error occurred. Please try again.');
            console.error('error:', err);
        }
    };

    return (
        <div className="container">
            <img src="piggy.png" alt="Piggy Bank" style={{ width: '100px', height: 'auto', marginBottom: '20px' }} />
            <h1 class="laughing-stock"><span class="pink">Laughing</span> <span class="orange">Stocks</span></h1>
            <h2 class="fin-ai">a financial <span class="purple">A</span>dv<span class="purple">I</span>sor</h2>
            <h2 class="pt2">for <span class="blue">Less Stress</span> and <span class="green">More Success</span></h2>

            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="username">Username </label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        value={formData.username}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <p></p>
                <div className="form-group">
                    <label htmlFor="password">Password </label>
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
                <p></p>
                <div className="form-group">
                    <button class="signup" type="submit">Sign up</button>
                </div>
            </form>
        </div>
    );
};

export default SignupPage; // Fixed export name (was exporting HomePage)
