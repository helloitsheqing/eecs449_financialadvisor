// InfoBank.js
import React, { useState } from 'react';

const InfoBankPage = () => {
    const [savedChats, setSavedChats] = useState([]);

    const handleSaveChat = (chat) => {
        setSavedChats((prevChats) => [...prevChats, chat]);
    };

    return (
        <div style={styles.container}>
            <p>Info Bank</p>
            <div style={styles.savedChats}>
                {savedChats.length === 0 ? (
                    <p>No chats saved yet.</p>
                ) : (
                    savedChats.map((chat, index) => (
                        <div key={index} style={styles.chat}>
                            <p>{chat}</p>
                        </div>
                    ))
                )}
            </div>
            <button style={styles.clearButton} onClick={() => setSavedChats([])}>
                Clear All Chats
            </button>
        </div>
    );
};

const styles = {
    container: {
        padding: '20px',
        backgroundColor: '#f1f8e9',
        borderRadius: '8px',
        maxWidth: '500px',
        margin: '20px auto',
        textAlign: 'center',
    },
    savedChats: {
        marginBottom: '20px',
    },
    chat: {
        padding: '10px',
        marginBottom: '10px',
        borderRadius: '5px',
        backgroundColor: '#c8e6c9',
        textAlign: 'center',
    },
    clearButton: {
        padding: '10px 20px',
        backgroundColor: '#f44336',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
    },
};

export default InfoBankPage;
