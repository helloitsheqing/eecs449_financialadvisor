// ChatPage.js
import React, { useContext, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import LogUserContext from './contexts/context.js';
import ExistingChatContext from './contexts/existingChatContext';
import { useNavigate } from 'react-router-dom';

const ExistingChatPage = () => {
    const { existingChat, setExistingChat } = useContext(ExistingChatContext);
    console.log("existingChat", existingChat);
    console.log("existingChat.conversation_data", existingChat.conversation_data);
    const [messages, setMessages] = useState(existingChat.conversation_data);
    console.log("messages", messages);
    const [inputValue, setInputValue] = useState('');
    const navigate = useNavigate();

    // const {username} = useContext(LogUserContext);
    // 1. TODO: Add Back button to home page
    // 2. TODO: ...

    console.log(messages);

    const handleBack = async () => {
        setExistingChat(-1); // clear context
        navigate('/infobank');
    };

    const handleSend = async () => {
        if (inputValue.trim() !== '') {
            setMessages((prevMessages) => [
                ...prevMessages,
                { text: inputValue, sender: 'user' },
            ]);
            console.log(messages);
            setInputValue('');

            try {
                const response = await axios.post(`http://localhost:5001/info_bank/chat/${existingChat.id}`, {
                    message: inputValue,
                    method: "POST",
                    credentials: 'include',
                });

                const botResponse = response.data.response;

                setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: botResponse, sender: 'bot' },
                ]);
            } catch (error) {
                console.error('Error:', error);
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: 'Error: Failed to get response from the bot.', sender: 'bot' },
                ]);
            }
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.header}>
                <button style={styles.backButton} onClick={handleBack}>
                    ← Back
                </button>
            </div>
            <div style={styles.chatWindow}>
                {messages.map((message, index) => (
                    <div
                        key={index}
                        style={{
                            ...styles.message,
                            ...(message.sender === 'user' ? styles.userMessage : styles.botMessage),
                        }}
                    >
                        {message.text}
                    </div>
                ))}
            </div>
            <div style={styles.inputContainer}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    style={styles.input}
                    placeholder="Type your message..."
                />
                <button onClick={handleSend} style={styles.sendButton}>
                    Send
                </button>
            </div>
        </div>
    );
};

const styles = {
    header: {
        display: 'flex',
        alignItems: 'center',
        padding: '10px 15px',
        backgroundColor: '#c8e6c9',
        borderBottom: '1px solid #a5d6a7',
    },

    backButton: {
        backgroundColor: 'transparent',
        border: 'none',
        color: '#2e7d32',
        fontSize: '16px',
        cursor: 'pointer',
        fontWeight: 'bold',
    },
    exchangeContainer: {
        marginBottom: '20px',
    },
    container: {
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        width: '100vw',
        backgroundColor: '#e0f7fa',
        overflow: 'hidden',
    },
    chatWindow: {
        flex: 1,
        padding: '20px',
        overflowY: 'auto',
        backgroundColor: '#f1f8e9',
        display: 'flex',
        flexDirection: 'column',
    },
    message: {
        padding: '15px',
        borderRadius: '10px',
        marginBottom: '10px',
        maxWidth: '80%',
        width: 'fit-content',
        wordWrap: 'break-word',
    },
    userMessage: {
        backgroundColor: '#c8e6c9',
        alignSelf: 'flex-end',
        marginLeft: '20%',
    },
    botMessage: {
        backgroundColor: '#a5d6a7',
        alignSelf: 'flex-start',
        marginRight: '20%',
    },
    inputContainer: {
        display: 'flex',
        padding: '15px',
        backgroundColor: '#c8e6c9',
        borderTop: '1px solid #a5d6a7',
    },
    input: {
        flex: 1,
        padding: '10px',
        borderRadius: '5px',
        border: 'none',
        marginRight: '10px',
        fontSize: '16px',
    },
    sendButton: {
        padding: '10px 20px',
        backgroundColor: '#4caf50',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        fontSize: '16px',
    },
    link: {
        marginTop: '10px',
        textDecoration: 'none',
        color: '#4caf50',
        fontSize: '16px',
    }
};

export default ExistingChatPage;
