import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
    const navigate = useNavigate(); // Hook to handle navigation

    const handleLoginClick = () => {
        navigate('/chat'); // Navigate to the chat screen when login is clicked
    };

    return (
        <div className="container">
            <h1>Laughing Stocks</h1>
            <h2>Your Financial Advisor for Less Stress and More Success</h2>
            <img src="piggy.png" alt="Piggy Bank" style={{ width: '100px', height: 'auto', marginBottom: '20px' }} />
            <button onClick={handleLoginClick}>Login</button>
            <button>Sign Up</button>
        </div>
    );
};

export default HomePage;
