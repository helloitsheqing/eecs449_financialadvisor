// InfoBank.js
import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import ExistingChatPage from './existingChatScreen.js';
import ExistingChatContext from './contexts/existingChatContext.js';
import LogUserContext from './contexts/context.js';


const InfoBankPage = () => {
    const [savedChats, setSavedChats] = useState([]);
    const [selectedChat, setSelectedChat] = useState(null);
    const { username } = useContext(LogUserContext);
    const { setExistingChat } = useContext(ExistingChatContext);
    const navigate = useNavigate();

    useEffect(() => {
        console.log("username: ", username);
        const fetchChats = async () => {
            try {
                const response = await fetch(`http://localhost:5001/info_bank/${username}/chats`, {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    // agent_model: "deepseek"
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const result = await response.json();
                if (result.success && result.data) {
                    setSavedChats(result.data);
                }
                console.log(result);
            } catch (error) {
                console.error("Error fetching chats:", error);
            }
        };
        fetchChats();
    }, []);

    const handleClearChat = async () => {
        try {
            const response = await fetch(`http://localhost:5001/info_bank/${username}/clear-chats`, {
                method: "DELETE",
                credentials: "include",
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log("Chats cleared:", result);
            setSavedChats([]);
            setSelectedChat(null);
        } catch (error) {
            console.error("Error clearing chats:", error);
            alert('Failed to clear chats. Please try again.');
        }
    };

    const handleViewChat = async (chatId) => {
        console.log('click');
        try {
            const response = await fetch(`http://localhost:5001/info_bank/${username}/chat/${chatId}`, {
                method: "GET",
                credentials: "include",
                // mode: "no-cors",
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                console.log("response: ", response);
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            if (result.success) {
                // NOTE:
                // current format:
                // [
                // {prompt: "question", response: "response"}
                // ]
                // parse result data into this format
                // [
                // { text: "question", sender: "user", }, { text: "response", sender: "bot", }, 
                // ]

                function parseChatData(data) {
                    const parsed = [];

                    data.forEach(pair => {
                        parsed.push({ text: pair.prompt, sender: "user" });
                        parsed.push({ text: pair.response, sender: "bot" });
                    });

                    return parsed;
                }
                console.log("prev");
                console.log(result.data.conversation_data);
                const parsedData = parseChatData(result.data.conversation_data);
                console.log("current");
                console.log(parsedData);

                // change result.data.conversation_data to parsedData
                result.data.conversation_data = parsedData
                setSelectedChat(result.data);

                setExistingChat(result.data);

                navigate('/existing-chat');
                console.log("result: ", result);
            }
        } catch (error) {
            console.error("Error fetching chat:", error);
        }
    };

    return (
        <div style={styles.container}>
            <h2>Info Bank</h2>
            <div style={styles.chatList}>
                {savedChats.length === 0 ? (
                    <p>No chats saved yet.</p>
                ) : (
                    <ul style={styles.chatListUl}>
                        {savedChats.map((chat) => (
                            <li key={chat.id} style={styles.chatListItem}>
                                <button
                                    style={styles.chatTitleButton}
                                    onClick={() => handleViewChat(chat.id)}
                                >
                                    {chat.conversation_title || "Untitled Conversation"}
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            {selectedChat && (
                <div style={styles.chatView}>
                    <h3>{selectedChat.conversation_title || "Untitled Conversation"}</h3>
                    <div style={styles.messagesContainer}>
                        {/* {JSON.parse(selectedChat.conversation_data).map((message, index) => (
                            <div key={index} style={styles.message}>
                                <strong>User:</strong> {message.prompt}
                                <br />
                                <strong>Bot:</strong> {message.response}
                            </div>
                        ))} */}
                    </div>
                </div>
            )}

            {savedChats.length > 0 && (
                <button style={styles.clearButton} onClick={handleClearChat}>
                    Clear All Chats
                </button>
            )}
        </div>
    );
};

// <ExistingChatPage existingMessages={selectedChat?.conversation_data || []} />
const styles = {
    container: {
        padding: '20px',
        backgroundColor: '#f1f8e9',
        borderRadius: '8px',
        maxWidth: '800px',
        margin: '20px auto',
    },
    chatList: {
        marginBottom: '20px',
    },
    chatListUl: {
        listStyle: 'none',
        padding: 0,
    },
    chatListItem: {
        marginBottom: '8px',
    },
    chatTitleButton: {
        padding: '8px 12px',
        backgroundColor: '#4caf50',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        width: '100%',
        textAlign: 'left',
    },
    chatView: {
        marginTop: '20px',
        padding: '15px',
        backgroundColor: '#e8f5e9',
        borderRadius: '5px',
    },
    messagesContainer: {
        marginTop: '10px',
    },
    message: {
        padding: '10px',
        marginBottom: '10px',
        backgroundColor: '#c8e6c9',
        borderRadius: '4px',
    },
    clearButton: {
        padding: '10px 20px',
        backgroundColor: '#f44336',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        marginTop: '20px',
    },
};

export default InfoBankPage;
