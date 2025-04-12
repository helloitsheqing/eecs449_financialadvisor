// Settings.js
import React, { useState } from 'react';

const Settings = () => {
    const [aiModel, setAiModel] = useState('deepseek-r1:1.5b');

    const handleModelChange = (event) => {
        setAiModel(event.target.value);
    };

    return (
        <div style={styles.container}>
            <h2>AI Model Settings</h2>
            <p>Current AI Model: {aiModel}</p>
            <select onChange={handleModelChange} value={aiModel} style={styles.select}>
                <option value="deepseek-r1:1.5b">DeepSeek R1</option>
                <option value="gemma3:1b">Gemma 3</option>
                <option value="mistral">Mistral</option>
                <option value="llama3.3">Llama 3</option>
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
