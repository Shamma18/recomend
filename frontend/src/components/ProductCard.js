import React from 'react';

const ProductCard = ({ product }) => {
  // Use a placeholder image if the one from the data is missing or broken
  const imageUrl = product.images && product.images[0] ? product.images[0] : 'https://via.placeholder.com/300';

  return (
    <div className="product-card">
      <div className="product-image-container">
        <img src={imageUrl} alt={product.title} className="product-image" />
      </div>
      <div className="product-info">
        <h4 className="product-title">{product.title}</h4>
        {/* THIS IS THE FIX: We are now using the 'genai_description' from the backend */}
        <p className="product-description">{product.genai_description}</p>
        <p className="product-price">{product.price}</p>
      </div>
    </div>
  );
};

export default ProductCard;