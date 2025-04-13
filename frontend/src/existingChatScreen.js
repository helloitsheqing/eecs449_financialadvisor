// ChatPage.js
import React, { useContext, useState, useEffect } from 'react';
import axios from 'axios';
import LogUserContext from './contexts/context.js';
import ExistingChatContext from './contexts/existingChatContext';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';


const ExistingChatPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { existingChat, setExistingChat } = useContext(ExistingChatContext);
    const { username } = useContext(LogUserContext);

    // State initialization
    const [conversationId, setConversationId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');

    // Handle both context and location state
    useEffect(() => {
        if (location.state?.fromChat) {
            // Coming from default chat
            setConversationId(location.state.conversationId);
            setMessages(location.state.initialMessages);
        } else if (existingChat?.id) {
            // Coming from InfoBank
            setConversationId(existingChat.id);
            setMessages(existingChat.conversation_data);
        }
        console.log("conversation id:", conversationId);
        console.log("username:", username);
    }, [location.state, existingChat]);

    const handleSend = async () => {
        if (inputValue.trim() !== '') {

            setInputValue('');

            try {
                // Add user message immediately
                setMessages(prev => [...prev, { text: inputValue, sender: 'user' }]);

                const response = await axios.post(`http://localhost:5001/info_bank/${username}/chat/${conversationId}`, {
                    message: inputValue,
                    // agent_model: "deepseek"
                    // conversation_id: conversationId,
                    username: username
                }, {
                    withCredentials: true
                });

                console.log("response", response);

                // Add bot response
                setMessages(prev => [
                    ...prev,
                    { text: response.data.response, sender: 'bot' }
                ]);

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

    const handleBack = () => {
        if (location.state?.fromChat) {
            navigate('/chat');  // Back to default chat
        } else {
            navigate('/infobank');  // Back to InfoBank
        }
        setExistingChat(null);
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
