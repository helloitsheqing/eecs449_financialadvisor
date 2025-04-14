// Settings.js
import React, { createContext, useState, useContext } from 'react';
import ModelContext from './contexts/modelPreference';
import MenuBar from './MenuBar.js';


const Settings = () => {
    const { agent_model, setAgentModel } = useContext(ModelContext);

    const handleModelChange = (event) => {
        setAgentModel(event.target.value);
    }

    return (
        <div style={styles.container}>
            <MenuBar></MenuBar>
            <h2>AI Model Settings</h2>
            <p>Current AI Model: <strong>{agent_model}</strong></p>
            <select 
                onChange={handleModelChange} 
                value={agent_model} 
                style={styles.select}
            >
                <option value="deepseek-r1:1.5b">DeepSeek R1</option>
                <option value="gemma">Gemma 3</option>
                <option value="mistral">Mistral</option>
                <option value="llama3.2">Llama 3</option>
             </select>
        </div>
    );
};

const styles = {
    container: {
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
