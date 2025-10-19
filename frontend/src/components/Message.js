import React from 'react';
import ProductCard from './ProductCard';

const Message = ({ message }) => {
  const messageClass = message.isUser ? 'user-message' : 'bot-message';

  return (
    <div className={`message-wrapper ${messageClass}`}>
      {/* Add a bot avatar for non-user messages */}
      {!message.isUser && <div className="bot-avatar">AI</div>}
      
      <div className="message-content">
        {message.text && <p>{message.text}</p>}
        
        {message.isLoading && (
          <div className="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}
        
        {message.products && (
          <div className="products-grid">
            {message.products.map(product => (
              <ProductCard key={product.uniq_id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Message;