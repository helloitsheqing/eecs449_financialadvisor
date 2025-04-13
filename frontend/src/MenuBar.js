// MenuBar.js
import React from 'react';
import { Link } from 'react-router-dom';
import './MenuBar.css';

const MenuBar = () => {
    return (
        <div class="topnav">
            <Link to="/chat">Chat</Link>
            <Link to="/infobank">Info Bank</Link>
            <Link to="/settings">Settings</Link>
            <Link to="/upload-excel">Upload Spreadsheet</Link>
        </div>
    );
};

const styles = {
    menuBar: {
        display: 'flex',
        justifyContent: 'space-around',
        padding: '10px',
        backgroundColor: '#4caf50',
        color: 'white',
    },
    link: {
        textDecoration: 'none',
        color: 'white',
        fontSize: '18px',
        padding: '10px 20px',
        borderRadius: '5px',
    }
};

export default MenuBar;
