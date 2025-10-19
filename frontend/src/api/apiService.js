import axios from 'axios';

// The base URL for our FastAPI backend
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Connect to the Python backend
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getRecommendations = (prompt) => {
  // POST request to http://localhost:8000/api/recommendations/
  return apiClient.post('/recommendations/', { prompt });
};

export const getAnalyticsData = () => {
  // GET request to http://localhost:8000/api/analytics/
  return apiClient.get('/analytics/');
};