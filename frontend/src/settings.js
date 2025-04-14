// Settings.js
import React, { useContext } from 'react';
import MenuBar from './MenuBar.js';
import ModelContext from './contexts/modelContext.js';

const Settings = () => {
    // const [aiModel, setAiModel] = useState('deepseek-r1:1.5b');
    const { model } = useContext(ModelContext);
    const { setModel } = useContext(ModelContext);

    const handleModelChange = async (event) => {
        // setAiModel(event.target.value);
        const newModel = event.target.value
        setModel(newModel);
        try{
            const response = fetch(`http://localhost:5001/change-model/${newModel}`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            console.error("Error fetching chats:", error);
        }
    };

    return (
        <div style={styles.container}>
            <MenuBar></MenuBar>
            <h2>AI Model Settings</h2>
            <p>Current AI Model: {model}</p>
            <select onChange={handleModelChange} value={model} style={styles.select}>
                <option value="deepseek-r1:1.5b">DeepSeek R1:1.5b</option>
                <option value="deepseek-r1:7b">DeepSeek R1:7b</option>
                <option value="gemma3:1b">Gemma 3</option>
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
