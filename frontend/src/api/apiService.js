import axios from "axios";

const apiClient = axios.create({
  // This is the corrected URL for your live backend.
  baseURL: "https://recomend-backend.onrender.com/api",

  headers: {
    "Content-Type": "application/json",
  },
});

// ... rest of the file ...

export const getRecommendations = (prompt) => {
  // POST request to http://localhost:8000/api/recommendations/
  return apiClient.post("/recommendations/", { prompt });
};

export const getAnalyticsData = () => {
  // GET request to http://localhost:8000/api/analytics/
  return apiClient.get("/analytics/");
};
