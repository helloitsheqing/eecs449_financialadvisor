import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
    const navigate = useNavigate(); // Hook to handle navigation

    const handleLoginClick = () => {
        navigate('/login'); // Navigate to the chat screen when login is clicked
        /* this will be changed so that it takes you to the 
        actual login route. the login route will render a page
        that takes you to the chat page */
    };

    const handleSignUpClick = () => {
        navigate('/signup'); // You'll need to create this route
    };


    return (
        <div className="container">
            <h1 class="welcome">Welcome to</h1>
            <h1 class="laughing-stock"><span class="pink">Laughing</span> <span class="orange">Stocks</span></h1>
            <h2 class="fin-ai">a financial <span class="purple">A</span>dv<span class="purple">I</span>sor</h2>
            <h2 class="pt2">for <span class="blue">Less Stress</span> and <span class="green">More Success</span></h2>
            <img src="piggy.png" alt="Piggy Bank" style={{ width: '200px', height: 'auto', marginBottom: '20px' }} />
            <button class="login" onClick={handleLoginClick}>Login</button>
            <button class="signup" onClick={handleSignUpClick}>Sign Up</button>
        </div>
    );
};

export default HomePage;
