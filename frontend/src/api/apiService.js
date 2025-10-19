import axios from "axios";

const apiClient = axios.create({
  // ⬇️ THIS IS THE MOST IMPORTANT CHANGE ⬇️
  // Replace the localhost URL with your live Render backend URL
  baseURL: "https://recomend-backend.onrender.comk",

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
