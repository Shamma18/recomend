import React, { useEffect, useState } from 'react';
import { getAnalyticsData } from '../api/apiService';

const AnalyticsDashboard = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getAnalyticsData();
        setData(response.data);
      } catch (err) {
        setError('Failed to fetch analytics data.');
        console.error(err);
      }
    };
    fetchData();
  }, []);

  if (error) {
    return <p className="error">{error}</p>;
  }

  if (!data) {
    return <p>Loading analytics...</p>;
  }

  return (
    <div className="analytics-dashboard">
      <div className="stat-card">
        <h3>Total Products</h3>
        <p>{data.total_products}</p>
      </div>
      <div className="stat-card">
        <h3>Average Price</h3>
        <p>${data.average_price.toFixed(2)}</p>
      </div>
      <div className="stat-card full-width">
        <h3>Products by Category</h3>
        <ul>
          {Object.entries(data.products_by_category).map(([category, count]) => (
            <li key={category}><strong>{category}:</strong> {count}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;