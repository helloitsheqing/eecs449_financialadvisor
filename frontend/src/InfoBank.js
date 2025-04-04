// InfoBank.js
import React, { useState } from 'react';

const InfoBankPage = () => {
    /* 
    we have an endpoint for extracting all chats
    how do we set up this component so that it makes use of that endpoint to get
    information for all chats
    */

    const [savedChats, setSavedChats] = useState([]);

    const handleSaveChat = (chat) => {
        setSavedChats((prevChats) => [...prevChats, chat]);
    };

    const handleClearChat = async (chat) => {
        setSavedChats([]);

        try {
            const response = await fetch(`http://localhost:5001/clear-chats`, {
                method: "DELETE",
                credentials: "include",
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok){
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log("Chats cleared:", result);
        } catch (error) {
            console.error("Error clearing chats:", error);
            // Revert state if API call fails
            setSavedChats(prevChats => [...prevChats]);
            alert('Failed to clear chats. Please try again.');
        }    
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
            <button style={styles.clearButton} onClick={handleClearChat}> 
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
