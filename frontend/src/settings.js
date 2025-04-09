// Settings.js
import React, { useState } from 'react';

const Settings = () => {
    const [aiModel, setAiModel] = useState('Model A');

    const handleModelChange = (event) => {
        setAiModel(event.target.value);
    };

    return (
        <div style={styles.container}>
            <h2>Settings</h2>
            <p>Current AI Model: {aiModel}</p>
            <select onChange={handleModelChange} value={aiModel} style={styles.select}>
                <option value="Model A">Model A</option>
                <option value="Model B">Model B</option>
            </select>
        </div>
    );
};

const styles = {
    container: {
        padding: '20px',
        textAlign: 'center',
    },
    select: {
        padding: '10px',
        fontSize: '16px',
        cursor: 'pointer',
        backgroundColor: 'white',
        border: '1px solid #4caf50',
        borderRadius: '5px',
        marginTop: '10px',
    }
};

export default Settings;
