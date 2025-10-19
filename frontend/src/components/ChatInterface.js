import React, { useState, useEffect, useRef } from 'react';
import { getRecommendations } from '../api/apiService';
import Message from './Message';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { isUser: false, text: "Hello! I'm your AI furniture assistant. What are you looking for today?" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const chatWindowRef = useRef(null);

  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { isUser: true, text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await getRecommendations(input);
      const botMessage = { isUser: false, products: response.data };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { isUser: false, text: "I'm sorry, I encountered an error. Please try your search again." };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-window" ref={chatWindowRef}>
        {messages.map((msg, index) => (
          <Message key={index} message={msg} />
        ))}
        {isLoading && <Message message={{ isUser: false, isLoading: true }} />}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="e.g., 'a comfortable sofa for a small apartment'"
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>Send</button>
      </div>
    </div>
  );
};

export default ChatInterface;