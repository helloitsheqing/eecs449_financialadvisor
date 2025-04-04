// MenuBar.js
import React from 'react';
import { Link } from 'react-router-dom';

const MenuBar = () => {
    return (
        <div style={styles.menuBar}>
            <Link to="/chat" style={styles.link}>Chat</Link>
            <Link to="/infobank" style={styles.link}>Info Bank</Link>
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
