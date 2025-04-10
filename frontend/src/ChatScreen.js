// ChatPage.js
import React, { useContext, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import LogUserContext from './contexts/context.js';

const ChatPage = () => {
    const navigate = useNavigate();
    const { username } = useContext(LogUserContext);
    const [inputValue, setInputValue] = useState('');
    
    // Initialize messages state with empty array
    const [messages, setMessages] = useState([]);

    const handleSend = async () => {
        if (inputValue.trim() !== ''){
            // setMessages((prevMessages) => [
            //     ...prevMessages,
            //     { text: inputValue, sender: 'user' },
            // ]);
            setInputValue('');

            console.log(messages); // state

            try {
                // Generate conversation ID only once per conversation
                
                // Add user message immediately to local state
                setMessages(prev => [
                    ...prev,
                    { text: inputValue, sender: 'user' }
                ]);

                const response = await axios.post(`http://localhost:5001/chat/${username}`, {
                    message: inputValue,
                    // conversation_id: conversationId,
                    username: username
                }, {
                    withCredentials: true
                });

                // Add bot response to local state
                setMessages(prev => [
                    ...prev,
                    { 
                        text: response.data.response, 
                        sender: 'bot',
                        // conversationId
                    }
                ]);

                // Handle first message redirect
                navigate('/existing-chat', {
                    state: {
                        fromChat: true,
                        conversationId: response.data.conversation_id,
                        initialMessages: [
                            { text: inputValue, sender: 'user' },
                            { text: response.data.response, sender: 'bot' }
                        ]
                    }
                });
                setInputValue('');

            } catch (error) {
                console.error('Error:', error);
                setMessages(prev => [
                    ...prev,
                    { text: 'Error: Failed to get response', sender: 'bot' }
                ]);
            }
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.chatWindow}>
                {/* Safe mapping since messages is always an array */}
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

// Your existing styles object remains the same
const styles = {
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
    }
};

export default ChatPage;