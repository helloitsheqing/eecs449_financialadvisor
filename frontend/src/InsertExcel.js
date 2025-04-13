// InsertExcel.js
import React, { useState } from 'react';
import axios from 'axios';
import MenuBar from './MenuBar.js';

const InsertExcel = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [promptText, setPromptText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [statusMessage, setStatusMessage] = useState('');

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handlePromptChange = (event) => {
        setPromptText(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        
        if (!selectedFile || !promptText) {
            setStatusMessage('Both file and prompt are required!');
            return;
        }
    
        setIsLoading(true);
        setStatusMessage('');
    
        try {
            const formData = new FormData();
            formData.append('excelFile', selectedFile);
            formData.append('prompt', promptText);

            for (let [key, value] of formData.entries()) {
                console.log(key, value);
            }
            
            
            // Proper way to send FormData with axios
            const response = await axios.post('http://localhost:5001/upload-excel', 
                formData,
                {
                    withCredentials: true,
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            );
    
            setStatusMessage(response.data.message || 'Upload successful!');
            setSelectedFile(null);
            setPromptText('');
        } catch (error) {
            setStatusMessage(`Error: ${error.response?.data?.message || error.message}`);
        } finally {
            setIsLoading(false);
        }
    };
    
    return (
        <div style={styles.container}>
            <MenuBar></MenuBar>
            <h2 style={styles.heading}>Insert Excel File</h2>
            <form onSubmit={handleSubmit} style={styles.form}>
                <div style={styles.formGroup}>
                    <label style={styles.label}>
                        Select Excel File:
                        <input
                            type="file"
                            onChange={handleFileChange}
                            accept=".xlsx,.xls,.csv"
                            required
                            style={styles.fileInput}
                        />
                    </label>
                </div>

                <div style={styles.formGroup}>
                    <label style={styles.label}>
                        Enter Prompt:
                        <textarea
                            value={promptText}
                            onChange={handlePromptChange}
                            required
                            style={styles.textarea}
                            placeholder="Enter your processing instructions..."
                        />
                    </label>
                </div>

                <button 
                    type="submit" 
                    style={styles.submitButton}
                    disabled={isLoading}
                >
                    {isLoading ? 'Processing...' : 'Upload & Process'}
                </button>

                {statusMessage && (
                    <div style={styles.statusMessage}>
                        {statusMessage}
                    </div>
                )}

                {isLoading && <div style={styles.loader}></div>}
            </form>
        </div>
    );
};

const styles = {
    container: {
        backgroundColor: '#f8f9fa',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    },
    heading: {
        textAlign: 'center',
        color: '#2c3e50',
        marginBottom: '2rem'
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        gap: '1.5rem'
    },
    formGroup: {
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem'
    },
    label: {
        fontSize: '1rem',
        color: '#34495e',
        fontWeight: '500'
    },
    fileInput: {
        display: 'block',
        marginTop: '0.5rem',
        padding: '0.5rem',
        border: '1px solid #bdc3c7',
        borderRadius: '4px'
    },
    textarea: {
        width: '100%',
        height: '100px',
        marginTop: '0.5rem',
        padding: '0.8rem',
        border: '1px solid #bdc3c7',
        borderRadius: '4px',
        resize: 'vertical'
    },
    submitButton: {
        backgroundColor: '#3498db',
        color: 'white',
        padding: '0.8rem 1.5rem',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '1rem',
        transition: 'background-color 0.2s',
        ':hover': {
            backgroundColor: '#2980b9'
        },
        ':disabled': {
            backgroundColor: '#7f8c8d',
            cursor: 'not-allowed'
        }
    },
    statusMessage: {
        marginTop: '1rem',
        padding: '1rem',
        borderRadius: '4px',
        backgroundColor: '#ecf0f1',
        color: '#2c3e50',
        textAlign: 'center'
    },
    loader: {
        margin: '1rem auto',
        border: '4px solid #f3f3f3',
        borderTop: '4px solid #3498db',
        borderRadius: '50%',
        width: '30px',
        height: '30px',
        animation: 'spin 1s linear infinite',
    },
    '@keyframes spin': {
        '0%': { transform: 'rotate(0deg)' },
        '100%': { transform: 'rotate(360deg)' }
    }
};

export default InsertExcel;